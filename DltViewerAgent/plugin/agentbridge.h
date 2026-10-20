#ifndef AGENTBRIDGE_H
#define AGENTBRIDGE_H

#include <QJsonObject>
#include <QList>
#include <QObject>
#include <QPointer>
#include <QTcpServer>
#include <QTcpSocket>
#include <atomic>
#include <memory>

class QDltFile;
class QDltMsg;
class QDltMessageDecoder;
class QTableView;
template <typename T> class QFutureWatcher;

QJsonObject dltMessageToJson(int index, const QDltMsg &msg, int maxPayloadChars);

// Localhost JSON-lines bridge between DLT Viewer and the agent process.
// Agent -> viewer: {"id":N,"method":...,"params":{...}} answered by {"id":N,"result"|"error":...}
// Either direction: {"event":name,...}. The first agent line must be {"type":"hello","token":...}.
class AgentBridge : public QObject
{
    Q_OBJECT

public:
    explicit AgentBridge(QObject *parent = nullptr);
    ~AgentBridge() override;

    bool listen();
    quint16 port() const;
    QString token() const;
    bool isAgentConnected() const;

    void setFile(QDltFile *file);
    void setTableView(QTableView *view);
    void setMessageDecoder(QDltMessageDecoder *decoder);
    void setSelected(int index, const QJsonObject &message);
    void sendEvent(const QString &name, const QJsonObject &data = QJsonObject());
    QJsonObject jumpTo(const QJsonObject &params, QString &error);

signals:
    void agentConnected();
    void agentDisconnected();
    void agentEvent(const QString &name, const QJsonObject &data);

private slots:
    void onNewConnection();
    void onReadyRead();
    void onDisconnected();

private:
    void handleLine(const QByteArray &line);
    void handleRequest(qint64 id, const QString &method, const QJsonObject &params);
    void reply(qint64 id, const QJsonObject &result);
    void replyError(qint64 id, const QString &message);
    void writeJson(const QJsonObject &obj);
    void cancelWorkers();

    QJsonObject fileInfo() const;
    QJsonObject messagesAround(const QJsonObject &params, QString &error) const;
    QJsonObject rows(const QJsonObject &params, QString &error) const;
    void runAsync(qint64 id, const QString &method, const QJsonObject &params);

    QList<qint64> visibleIndices(bool filtered) const;
    int rowOfIndex(int index) const;
    QJsonObject readMessage(int index, int maxPayloadChars) const;

    QTcpServer m_server;
    QPointer<QTcpSocket> m_client;
    bool m_authenticated = false;
    QByteArray m_buffer;
    QString m_token;

    QDltFile *m_file = nullptr;
    QPointer<QTableView> m_table;
    QDltMessageDecoder *m_decoder = nullptr;
    int m_selectedIndex = -1;
    QJsonObject m_selectedMessage;

    std::shared_ptr<std::atomic_bool> m_cancel;
    QList<QFutureWatcher<QJsonObject> *> m_workers;
};

#endif // AGENTBRIDGE_H
