#include "agentbridge.h"

#include <QAbstractItemModel>
#include <QFutureWatcher>
#include <QHash>
#include <QHeaderView>
#include <QItemSelectionModel>
#include <QJsonArray>
#include <QJsonDocument>
#include <QRandomGenerator>
#include <QRegularExpression>
#include <QTableView>
#include <QtConcurrent>
#include <algorithm>

#include "qdltfile.h"
#include "qdltmessagedecoder.h"
#include "qdltmsg.h"

namespace {

constexpr int kMaxLineBytes = 4 * 1024 * 1024;
constexpr int kListPayloadChars = 600;
constexpr int kFullPayloadChars = 8000;
constexpr int kMaxRows = 200;
constexpr int kMaxContext = 100;
constexpr int kMaxSearchResults = 200;
constexpr int kMaxGroups = 200;
constexpr int kCancelCheckInterval = 4096;

int boundedInt(const QJsonObject &params, const char *key, int fallback, int minValue, int maxValue)
{
    const QJsonValue value = params.value(QLatin1String(key));
    const int n = value.isDouble() ? value.toInt() : fallback;
    return std::clamp(n, minValue, maxValue);
}

// Rows of either the whole file or the current filter result, without copying the whole file.
struct Scope
{
    bool all = true;
    int total = 0;
    QList<qint64> indices;

    int size() const { return all ? total : int(indices.size()); }
    int indexAt(int row) const { return all ? row : int(indices.at(row)); }
};

bool parseMessage(const QDltFile *file, int index, bool dltv2, QDltMsg &msg)
{
    const QByteArray bytes = file->getMsg(index);
    return !bytes.isEmpty() && msg.setMsg(bytes, true, dltv2);
}

QString searchableText(const QDltMsg &msg)
{
    return QStringLiteral("%1 %2 %3 %4 %5").arg(msg.getEcuid(), msg.getApid(), msg.getCtid(),
                                                  msg.getSubtypeString(), msg.toStringPayload());
}

QJsonObject runSearch(const QDltFile *file, bool dltv2, const Scope &scope, const QJsonObject &params,
                      const std::shared_ptr<std::atomic_bool> &cancel)
{
    const QString query = params.value(QStringLiteral("query")).toString();
    const bool useRegex = params.value(QStringLiteral("regex")).toBool(false);
    const bool caseSensitive = params.value(QStringLiteral("case_sensitive")).toBool(false);
    const int maxResults = boundedInt(params, "max_results", 50, 1, kMaxSearchResults);
    const int startRow = boundedInt(params, "start_row", 0, 0, std::max(0, scope.size()));
    const QString app = params.value(QStringLiteral("app")).toString();
    const QString ctx = params.value(QStringLiteral("ctx")).toString();
    QStringList levels;
    for (const QJsonValue &level : params.value(QStringLiteral("levels")).toArray())
        levels << level.toString().toLower();

    const Qt::CaseSensitivity cs = caseSensitive ? Qt::CaseSensitive : Qt::CaseInsensitive;
    QRegularExpression regex;
    if (useRegex) {
        regex.setPattern(query);
        if (!caseSensitive)
            regex.setPatternOptions(QRegularExpression::CaseInsensitiveOption);
        if (!regex.isValid())
            return {{QStringLiteral("error"), QStringLiteral("Invalid regex: %1").arg(regex.errorString())}};
    }

    QJsonArray matches;
    int row = startRow;
    for (; row < scope.size(); ++row) {
        if (row % kCancelCheckInterval == 0 && cancel->load())
            return {{QStringLiteral("error"), QStringLiteral("Cancelled")}};

        const int index = scope.indexAt(row);
        QDltMsg msg;
        if (!parseMessage(file, index, dltv2, msg))
            continue;
        if (!app.isEmpty() && msg.getApid() != app)
            continue;
        if (!ctx.isEmpty() && msg.getCtid() != ctx)
            continue;
        if (!levels.isEmpty() && !levels.contains(msg.getSubtypeString().toLower()))
            continue;
        if (!query.isEmpty()) {
            const QString text = searchableText(msg);
            if (useRegex ? !regex.match(text).hasMatch() : !text.contains(query, cs))
                continue;
        }

        QJsonObject hit = dltMessageToJson(index, msg, kListPayloadChars);
        hit.insert(QStringLiteral("row"), row);
        matches.append(hit);
        if (matches.size() >= maxResults) {
            ++row;
            break;
        }
    }

    const bool truncated = row < scope.size();
    QJsonObject result{{QStringLiteral("matches"), matches},
                       {QStringLiteral("rows_scanned"), row - startRow},
                       {QStringLiteral("total_rows"), scope.size()},
                       {QStringLiteral("truncated"), truncated}};
    if (truncated)
        result.insert(QStringLiteral("next_start_row"), row);
    return result;
}

QJsonObject runStatistics(const QDltFile *file, bool dltv2, const Scope &scope, const QJsonObject &params,
                          const std::shared_ptr<std::atomic_bool> &cancel)
{
    static const QStringList kGroupings{QStringLiteral("app_ctx"), QStringLiteral("app"), QStringLiteral("ctx"),
                                        QStringLiteral("ecu"), QStringLiteral("level"), QStringLiteral("type")};
    const QString groupBy = params.value(QStringLiteral("group_by")).toString(QStringLiteral("app_ctx"));
    if (!kGroupings.contains(groupBy))
        return {{QStringLiteral("error"), QStringLiteral("group_by must be one of: %1").arg(kGroupings.join(", "))}};
    const int top = boundedInt(params, "top", 30, 1, kMaxGroups);

    struct Group { int count = 0; int first = -1; int last = -1; };
    QHash<QString, Group> groups;
    QHash<QString, int> levels;
    int firstIndex = -1;
    int lastIndex = -1;
    int parsed = 0;

    for (int row = 0; row < scope.size(); ++row) {
        if (row % kCancelCheckInterval == 0 && cancel->load())
            return {{QStringLiteral("error"), QStringLiteral("Cancelled")}};

        const int index = scope.indexAt(row);
        QDltMsg msg;
        if (!parseMessage(file, index, dltv2, msg))
            continue;
        ++parsed;

        QString key;
        if (groupBy == QLatin1String("app_ctx")) key = msg.getApid() + QLatin1Char('/') + msg.getCtid();
        else if (groupBy == QLatin1String("app")) key = msg.getApid();
        else if (groupBy == QLatin1String("ctx")) key = msg.getCtid();
        else if (groupBy == QLatin1String("ecu")) key = msg.getEcuid();
        else if (groupBy == QLatin1String("level")) key = msg.getSubtypeString();
        else key = msg.getTypeString();

        Group &group = groups[key];
        if (group.first < 0)
            group.first = index;
        group.last = index;
        ++group.count;
        ++levels[msg.getTypeString() == QLatin1String("log") ? msg.getSubtypeString() : msg.getTypeString()];

        if (firstIndex < 0)
            firstIndex = index;
        lastIndex = index;
    }

    const auto timeOf = [&](int index) {
        QDltMsg msg;
        return (index >= 0 && parseMessage(file, index, dltv2, msg))
                   ? dltMessageToJson(index, msg, 0).value(QStringLiteral("time")).toString()
                   : QString();
    };

    QList<QPair<QString, Group>> sorted;
    sorted.reserve(groups.size());
    for (auto it = groups.cbegin(); it != groups.cend(); ++it)
        sorted.append({it.key(), it.value()});
    std::sort(sorted.begin(), sorted.end(), [](const auto &a, const auto &b) { return a.second.count > b.second.count; });

    QJsonArray groupArray;
    for (int i = 0; i < std::min(top, int(sorted.size())); ++i) {
        groupArray.append(QJsonObject{{QStringLiteral("key"), sorted[i].first},
                                      {QStringLiteral("count"), sorted[i].second.count},
                                      {QStringLiteral("first_index"), sorted[i].second.first},
                                      {QStringLiteral("last_index"), sorted[i].second.last}});
    }
    QJsonObject levelObject;
    for (auto it = levels.cbegin(); it != levels.cend(); ++it)
        levelObject.insert(it.key(), it.value());

    return {{QStringLiteral("group_by"), groupBy},
            {QStringLiteral("messages_counted"), parsed},
            {QStringLiteral("distinct_groups"), int(groups.size())},
            {QStringLiteral("groups"), groupArray},
            {QStringLiteral("level_counts"), levelObject},
            {QStringLiteral("first_time"), timeOf(firstIndex)},
            {QStringLiteral("last_time"), timeOf(lastIndex)}};
}

} // namespace

QJsonObject dltMessageToJson(int index, const QDltMsg &msg, int maxPayloadChars)
{
    QJsonObject obj{
        {QStringLiteral("index"), index},
        {QStringLiteral("time"), QStringLiteral("%1.%2").arg(msg.getTimeString()).arg(msg.getMicroseconds(), 6, 10, QLatin1Char('0'))},
        {QStringLiteral("uptime_s"), QString::number(msg.getTimestamp() / 10000.0, 'f', 4)},
        {QStringLiteral("ecu"), msg.getEcuid()},
        {QStringLiteral("app"), msg.getApid()},
        {QStringLiteral("ctx"), msg.getCtid()},
        {QStringLiteral("type"), msg.getTypeString()},
        {QStringLiteral("level"), msg.getSubtypeString()},
        {QStringLiteral("mode"), msg.getModeString()}};
    if (maxPayloadChars > 0) {
        QString payload = msg.toStringPayload();
        if (payload.size() > maxPayloadChars) {
            obj.insert(QStringLiteral("payload_truncated_from"), int(payload.size()));
            payload.truncate(maxPayloadChars);
        }
        obj.insert(QStringLiteral("payload"), payload);
    }
    return obj;
}

AgentBridge::AgentBridge(QObject *parent)
    : QObject(parent), m_cancel(std::make_shared<std::atomic_bool>(false))
{
    QByteArray secret(32, Qt::Uninitialized);
    QRandomGenerator::system()->fillRange(reinterpret_cast<quint32 *>(secret.data()), secret.size() / 4);
    m_token = QString::fromLatin1(secret.toHex());
    connect(&m_server, &QTcpServer::newConnection, this, &AgentBridge::onNewConnection);
}

AgentBridge::~AgentBridge()
{
    cancelWorkers();
    for (QFutureWatcher<QJsonObject> *watcher : std::as_const(m_workers))
        watcher->waitForFinished();
}

bool AgentBridge::listen()
{
    return m_server.isListening() || m_server.listen(QHostAddress::LocalHost, 0);
}

quint16 AgentBridge::port() const { return m_server.serverPort(); }
QString AgentBridge::token() const { return m_token; }
bool AgentBridge::isAgentConnected() const { return m_client && m_authenticated; }

void AgentBridge::setFile(QDltFile *file)
{
    cancelWorkers();
    m_file = file;
    m_selectedIndex = -1;
    m_selectedMessage = QJsonObject();
}

void AgentBridge::setTableView(QTableView *view) { m_table = view; }
void AgentBridge::setMessageDecoder(QDltMessageDecoder *decoder) { m_decoder = decoder; }

void AgentBridge::setSelected(int index, const QJsonObject &message)
{
    m_selectedIndex = index;
    m_selectedMessage = message;
}

void AgentBridge::sendEvent(const QString &name, const QJsonObject &data)
{
    QJsonObject obj = data;
    obj.insert(QStringLiteral("event"), name);
    writeJson(obj);
}

void AgentBridge::onNewConnection()
{
    while (QTcpSocket *socket = m_server.nextPendingConnection()) {
        if (m_client) {
            socket->abort();
            socket->deleteLater();
            continue;
        }
        m_client = socket;
        m_authenticated = false;
        m_buffer.clear();
        connect(socket, &QTcpSocket::readyRead, this, &AgentBridge::onReadyRead);
        connect(socket, &QTcpSocket::disconnected, this, &AgentBridge::onDisconnected);
    }
}

void AgentBridge::onReadyRead()
{
    if (!m_client)
        return;
    m_buffer.append(m_client->readAll());
    qsizetype newline;
    while (m_client && (newline = m_buffer.indexOf('\n')) >= 0) {
        const QByteArray line = m_buffer.left(newline).trimmed();
        m_buffer.remove(0, newline + 1);
        if (!line.isEmpty())
            handleLine(line);
    }
    if (m_client && m_buffer.size() > kMaxLineBytes)
        m_client->abort();
}

void AgentBridge::onDisconnected()
{
    cancelWorkers();
    const bool wasAuthenticated = m_authenticated;
    if (m_client)
        m_client->deleteLater();
    m_client = nullptr;
    m_authenticated = false;
    m_buffer.clear();
    if (wasAuthenticated)
        emit agentDisconnected();
}

void AgentBridge::handleLine(const QByteArray &line)
{
    QJsonParseError parseError;
    const QJsonDocument doc = QJsonDocument::fromJson(line, &parseError);
    if (parseError.error != QJsonParseError::NoError || !doc.isObject()) {
        if (!m_authenticated)
            m_client->abort();
        return;
    }
    const QJsonObject obj = doc.object();

    if (!m_authenticated) {
        if (obj.value(QStringLiteral("type")).toString() != QLatin1String("hello")
            || obj.value(QStringLiteral("token")).toString() != m_token) {
            m_client->abort();
            return;
        }
        m_authenticated = true;
        sendEvent(QStringLiteral("ready"), fileInfo());
        emit agentConnected();
        return;
    }

    if (obj.contains(QStringLiteral("id"))) {
        handleRequest(obj.value(QStringLiteral("id")).toInteger(), obj.value(QStringLiteral("method")).toString(),
                      obj.value(QStringLiteral("params")).toObject());
    } else if (obj.contains(QStringLiteral("event"))) {
        emit agentEvent(obj.value(QStringLiteral("event")).toString(), obj);
    }
}

void AgentBridge::handleRequest(qint64 id, const QString &method, const QJsonObject &params)
{
    if (method == QLatin1String("file_info")) {
        reply(id, fileInfo());
        return;
    }
    if (!m_file || m_file->size() == 0) {
        replyError(id, QStringLiteral("No DLT file is loaded in DLT Viewer."));
        return;
    }

    QString error;
    QJsonObject result;
    if (method == QLatin1String("get_selected")) {
        if (m_selectedIndex < 0) {
            replyError(id, QStringLiteral("No message is selected in DLT Viewer."));
            return;
        }
        result = readMessage(m_selectedIndex, kFullPayloadChars);
        if (result.isEmpty())
            result = m_selectedMessage;
    } else if (method == QLatin1String("get_message")) {
        const int index = params.value(QStringLiteral("index")).toInt(-1);
        result = readMessage(index, kFullPayloadChars);
        if (result.isEmpty())
            error = QStringLiteral("Message %1 does not exist or could not be parsed.").arg(index);
    } else if (method == QLatin1String("messages_around")) {
        result = messagesAround(params, error);
    } else if (method == QLatin1String("rows")) {
        result = rows(params, error);
    } else if (method == QLatin1String("jump_to")) {
        result = jumpTo(params, error);
    } else if (method == QLatin1String("search") || method == QLatin1String("statistics")) {
        runAsync(id, method, params);
        return;
    } else {
        error = QStringLiteral("Unknown method: %1").arg(method);
    }

    if (error.isEmpty())
        reply(id, result);
    else
        replyError(id, error);
}

void AgentBridge::reply(qint64 id, const QJsonObject &result)
{
    writeJson({{QStringLiteral("id"), id}, {QStringLiteral("result"), result}});
}

void AgentBridge::replyError(qint64 id, const QString &message)
{
    writeJson({{QStringLiteral("id"), id}, {QStringLiteral("error"), message}});
}

void AgentBridge::writeJson(const QJsonObject &obj)
{
    if (!isAgentConnected())
        return;
    m_client->write(QJsonDocument(obj).toJson(QJsonDocument::Compact));
    m_client->write("\n");
}

void AgentBridge::cancelWorkers()
{
    m_cancel->store(true);
    m_cancel = std::make_shared<std::atomic_bool>(false);
}

QJsonObject AgentBridge::fileInfo() const
{
    QJsonArray files;
    if (m_file) {
        for (int i = 0; i < m_file->getNumberOfFiles(); ++i)
            files.append(m_file->getFileName(i));
    }
    return {{QStringLiteral("files"), files},
            {QStringLiteral("total_messages"), m_file ? m_file->size() : 0},
            {QStringLiteral("filter_active"), m_file && m_file->isFilter()},
            {QStringLiteral("visible_messages"), m_file ? (m_file->isFilter() ? m_file->sizeFilter() : m_file->size()) : 0},
            {QStringLiteral("selected_index"), m_selectedIndex}};
}

QList<qint64> AgentBridge::visibleIndices(bool filtered) const
{
    return (filtered && m_file->isFilter()) ? m_file->getIndexFilter() : QList<qint64>();
}

int AgentBridge::rowOfIndex(int index) const
{
    if (!m_file->isFilter())
        return index;
    const QList<qint64> indices = m_file->getIndexFilter();
    const qsizetype exact = indices.indexOf(index);
    if (exact >= 0)
        return int(exact);
    // Not visible under the current filter: use the nearest earlier visible message, like DLT Viewer's jump.
    qint64 best = -1;
    qsizetype bestRow = indices.isEmpty() ? -1 : 0;
    for (qsizetype row = 0; row < indices.size(); ++row) {
        if (indices[row] <= index && indices[row] > best) {
            best = indices[row];
            bestRow = row;
        }
    }
    return int(bestRow);
}

QJsonObject AgentBridge::readMessage(int index, int maxPayloadChars) const
{
    if (index < 0 || index >= m_file->size())
        return QJsonObject();
    QDltMsg msg;
    if (!parseMessage(m_file, index, m_file->getDLTv2Support(), msg))
        return QJsonObject();
    if (m_decoder)
        m_decoder->decodeMsg(msg, 0);
    return dltMessageToJson(index, msg, maxPayloadChars);
}

QJsonObject AgentBridge::messagesAround(const QJsonObject &params, QString &error) const
{
    const int index = params.value(QStringLiteral("index")).toInt(-1);
    if (index < 0 || index >= m_file->size()) {
        error = QStringLiteral("index must be between 0 and %1").arg(m_file->size() - 1);
        return QJsonObject();
    }
    const bool filtered = params.value(QStringLiteral("filtered")).toBool(true) && m_file->isFilter();
    const int before = boundedInt(params, "before", 10, 0, kMaxContext);
    const int after = boundedInt(params, "after", 10, 0, kMaxContext);

    const QList<qint64> indices = visibleIndices(filtered);
    const int total = filtered ? int(indices.size()) : m_file->size();
    const int centerRow = filtered ? rowOfIndex(index) : index;

    QJsonArray messages;
    for (int row = std::max(0, centerRow - before); row <= std::min(total - 1, centerRow + after); ++row) {
        const QJsonObject msg = readMessage(filtered ? int(indices[row]) : row, kListPayloadChars);
        if (!msg.isEmpty())
            messages.append(msg);
    }
    return {{QStringLiteral("requested_index"), index},
            {QStringLiteral("requested_index_visible"), !filtered || indices.contains(index)},
            {QStringLiteral("view"), filtered ? QStringLiteral("filtered") : QStringLiteral("all")},
            {QStringLiteral("messages"), messages}};
}

QJsonObject AgentBridge::rows(const QJsonObject &params, QString &error) const
{
    const bool filtered = params.value(QStringLiteral("filtered")).toBool(true) && m_file->isFilter();
    const QList<qint64> indices = visibleIndices(filtered);
    const int total = filtered ? int(indices.size()) : m_file->size();
    const int start = params.value(QStringLiteral("start_row")).toInt(0);
    if (start < 0 || start >= total) {
        error = QStringLiteral("start_row must be between 0 and %1").arg(total - 1);
        return QJsonObject();
    }
    const int count = boundedInt(params, "count", 50, 1, kMaxRows);

    QJsonArray messages;
    for (int row = start; row < std::min(total, start + count); ++row) {
        QJsonObject msg = readMessage(filtered ? int(indices[row]) : row, kListPayloadChars);
        if (msg.isEmpty())
            continue;
        msg.insert(QStringLiteral("row"), row);
        messages.append(msg);
    }
    return {{QStringLiteral("view"), filtered ? QStringLiteral("filtered") : QStringLiteral("all")},
            {QStringLiteral("total_rows"), total},
            {QStringLiteral("messages"), messages}};
}

QJsonObject AgentBridge::jumpTo(const QJsonObject &params, QString &error)
{
    if (!m_file || m_file->size() == 0) {
        error = QStringLiteral("No DLT file is loaded in DLT Viewer.");
        return QJsonObject();
    }
    const int index = params.value(QStringLiteral("index")).toInt(-1);
    if (index < 0 || index >= m_file->size()) {
        error = QStringLiteral("index must be between 0 and %1").arg(m_file->size() - 1);
        return QJsonObject();
    }
    if (!m_table || !m_table->model() || !m_table->selectionModel()) {
        error = QStringLiteral("The DLT Viewer message table is not available.");
        return QJsonObject();
    }
    const int row = rowOfIndex(index);
    QAbstractItemModel *model = m_table->model();
    if (row < 0 || row >= model->rowCount()) {
        error = QStringLiteral("Message %1 is not in the current view.").arg(index);
        return QJsonObject();
    }
    int column = 0;
    while (column < model->columnCount() && m_table->isColumnHidden(column))
        ++column;

    const QModelIndex target = model->index(row, column);
    m_table->scrollTo(target, QAbstractItemView::PositionAtCenter);
    m_table->selectionModel()->select(target, QItemSelectionModel::ClearAndSelect | QItemSelectionModel::Rows);
    m_table->setCurrentIndex(target);
    return {{QStringLiteral("jumped_to_row"), row},
            {QStringLiteral("exact"), !m_file->isFilter() || m_file->getIndexFilter().contains(index)}};
}

void AgentBridge::runAsync(qint64 id, const QString &method, const QJsonObject &params)
{
    Scope scope;
    const bool filtered = params.value(QStringLiteral("filtered")).toBool(true) && m_file->isFilter();
    scope.all = !filtered;
    scope.total = m_file->size();
    if (filtered)
        scope.indices = m_file->getIndexFilter();

    const QDltFile *file = m_file;
    const bool dltv2 = m_file->getDLTv2Support();
    const auto cancel = m_cancel;
    const bool isSearch = method == QLatin1String("search");

    auto *watcher = new QFutureWatcher<QJsonObject>(this);
    m_workers.append(watcher);
    const QPointer<QTcpSocket> requester = m_client;
    connect(watcher, &QFutureWatcher<QJsonObject>::finished, this, [this, watcher, requester, id, filtered]() {
        m_workers.removeOne(watcher);
        watcher->deleteLater();
        if (!requester || requester != m_client)
            return;
        QJsonObject result = watcher->result();
        if (result.contains(QStringLiteral("error"))) {
            replyError(id, result.value(QStringLiteral("error")).toString());
            return;
        }
        result.insert(QStringLiteral("view"), filtered ? QStringLiteral("filtered") : QStringLiteral("all"));
        reply(id, result);
    });
    watcher->setFuture(QtConcurrent::run([file, dltv2, scope, params, cancel, isSearch]() {
        return isSearch ? runSearch(file, dltv2, scope, params, cancel)
                        : runStatistics(file, dltv2, scope, params, cancel);
    }));
}
