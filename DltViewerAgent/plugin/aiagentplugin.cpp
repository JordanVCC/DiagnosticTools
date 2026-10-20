#include "aiagentplugin.h"

#include <QCoreApplication>
#include <QDir>
#include <QFileInfo>
#include <QJsonObject>
#include <QProcessEnvironment>

#include "agentbridge.h"
#include "agentpanel.h"

namespace {

constexpr int kMaxStderrBytes = 8192;

// Default layout: <DltViewerAgent>/build/bin/dlt-viewer.exe and <DltViewerAgent>/agent/dlt_agent.py.
QString agentDirectory()
{
    const QString overridden = qEnvironmentVariable("DLT_AGENT_DIR");
    if (!overridden.isEmpty())
        return QDir::cleanPath(overridden);
    return QDir::cleanPath(QCoreApplication::applicationDirPath() + QStringLiteral("/../../agent"));
}

} // namespace

AiAgentPlugin::AiAgentPlugin()
    : m_bridge(new AgentBridge(this))
{
    connect(m_bridge, &AgentBridge::agentConnected, this, [this]() {
        if (m_panel)
            m_panel->setStatus(tr("Agent connected."));
        flushPendingPrompts();
    });
    connect(m_bridge, &AgentBridge::agentDisconnected, this, [this]() {
        if (m_panel)
            m_panel->setStatus(tr("Agent disconnected."));
        setTurnActive(false);
    });
    connect(m_bridge, &AgentBridge::agentEvent, this, &AiAgentPlugin::onAgentEvent);
}

AiAgentPlugin::~AiAgentPlugin()
{
    stopAgent();
}

QString AiAgentPlugin::name() { return QStringLiteral("AI Agent Plugin"); }
QString AiAgentPlugin::pluginVersion() { return QStringLiteral(AI_AGENT_PLUGIN_VERSION); }
QString AiAgentPlugin::pluginInterfaceVersion() { return QStringLiteral(PLUGIN_INTERFACE_VERSION); }
QString AiAgentPlugin::description() { return tr("Chat with a Copilot agent that can read and navigate the open DLT log."); }
QString AiAgentPlugin::error() { return m_error; }
bool AiAgentPlugin::loadConfig(QString) { return true; }
bool AiAgentPlugin::saveConfig(QString) { return true; }
QStringList AiAgentPlugin::infoConfig() { return {tr("Agent directory: %1").arg(agentDirectory())}; }

QWidget *AiAgentPlugin::initViewer()
{
    m_panel = new AgentPanel();
    m_panel->setStatus(tr("Agent not started. It starts when you send the first message."));
    connect(m_panel, &AgentPanel::promptSubmitted, this, &AiAgentPlugin::onPrompt);
    connect(m_panel, &AgentPanel::stopRequested, this, [this]() { m_bridge->sendEvent(QStringLiteral("abort")); });
    connect(m_panel, &AgentPanel::newChatRequested, this, [this]() {
        m_panel->clearTranscript();
        m_bridge->sendEvent(QStringLiteral("reset"));
    });
    connect(m_panel, &AgentPanel::jumpRequested, this, [this](int index) {
        QString jumpError;
        m_bridge->jumpTo(QJsonObject{{QStringLiteral("index"), index}}, jumpError);
        if (!jumpError.isEmpty() && m_panel)
            m_panel->appendError(jumpError);
    });
    return m_panel;
}

void AiAgentPlugin::initFileStart(QDltFile *file)
{
    m_file = file;
    m_bridge->setFile(file);
    if (m_panel)
        m_panel->setSelectedIndex(-1);
}

void AiAgentPlugin::initFileFinish() {}
void AiAgentPlugin::initMsg(int, QDltMsg &) {}
void AiAgentPlugin::initMsgDecoded(int, QDltMsg &) {}
void AiAgentPlugin::updateFileStart() {}
void AiAgentPlugin::updateMsg(int, QDltMsg &) {}
void AiAgentPlugin::updateMsgDecoded(int, QDltMsg &) {}
void AiAgentPlugin::updateFileFinish() {}
void AiAgentPlugin::selectedIdxMsg(int, QDltMsg &) {}

void AiAgentPlugin::selectedIdxMsgDecoded(int index, QDltMsg &msg)
{
    m_bridge->setSelected(index, dltMessageToJson(index, msg, 8000));
    if (m_panel)
        m_panel->setSelectedIndex(index);
}

bool AiAgentPlugin::initControl(QDltControl *) { return true; }
bool AiAgentPlugin::initConnections(QStringList) { return true; }
bool AiAgentPlugin::controlMsg(int, QDltMsg &) { return true; }
bool AiAgentPlugin::stateChanged(int, QDltConnection::QDltConnectionState, QString) { return true; }
bool AiAgentPlugin::autoscrollStateChanged(bool) { return true; }
void AiAgentPlugin::initMessageDecoder(QDltMessageDecoder *messageDecoder) { m_bridge->setMessageDecoder(messageDecoder); }
void AiAgentPlugin::initMainTableView(QTableView *pTableView) { m_bridge->setTableView(pTableView); }
void AiAgentPlugin::configurationChanged() {}

void AiAgentPlugin::onPrompt(const QString &text)
{
    if (!m_file || m_file->size() == 0) {
        m_panel->appendError(tr("Open a DLT file first."));
        return;
    }
    m_panel->appendUser(text);
    setTurnActive(true);
    m_pendingPrompts.append(text);
    if (m_bridge->isAgentConnected())
        flushPendingPrompts();
    else
        startAgent();
}

void AiAgentPlugin::onAgentEvent(const QString &name, const QJsonObject &data)
{
    if (!m_panel)
        return;
    const QString text = data.value(QStringLiteral("text")).toString();
    if (name == QLatin1String("assistant_delta"))
        m_panel->appendAssistantDelta(text);
    else if (name == QLatin1String("assistant_message"))
        m_panel->setAssistantMessage(text);
    else if (name == QLatin1String("tool"))
        m_panel->appendTool(text);
    else if (name == QLatin1String("status"))
        m_panel->setStatus(text);
    else if (name == QLatin1String("error"))
        m_panel->appendError(text);
    else if (name == QLatin1String("turn_end"))
        setTurnActive(false);
}

void AiAgentPlugin::startAgent()
{
    if (m_agent && m_agent->state() != QProcess::NotRunning)
        return;

    const QString dir = agentDirectory();
    const QString python = dir + QStringLiteral("/.venv/Scripts/python.exe");
    const QString script = dir + QStringLiteral("/dlt_agent.py");
    if (!QFileInfo::exists(python) || !QFileInfo::exists(script)) {
        m_panel->appendError(tr("Agent not found. Expected %1 and %2 (set DLT_AGENT_DIR to override).").arg(python, script));
        m_pendingPrompts.clear();
        setTurnActive(false);
        return;
    }
    if (!m_bridge->listen()) {
        m_panel->appendError(tr("Could not open the local agent connection."));
        m_pendingPrompts.clear();
        setTurnActive(false);
        return;
    }

    if (!m_agent) {
        m_agent = new QProcess(this);
        connect(m_agent, &QProcess::readyReadStandardError, this, [this]() {
            m_agentStderr.append(m_agent->readAllStandardError());
            if (m_agentStderr.size() > kMaxStderrBytes)
                m_agentStderr = m_agentStderr.right(kMaxStderrBytes);
        });
        connect(m_agent, &QProcess::finished, this, [this](int exitCode, QProcess::ExitStatus) {
            if (m_panel && exitCode != 0) {
                const QString tail = QString::fromUtf8(m_agentStderr).trimmed().right(1500);
                m_panel->appendError(tr("Agent exited (code %1). %2").arg(exitCode).arg(tail));
            }
            if (m_panel)
                m_panel->setStatus(tr("Agent stopped. It restarts when you send a message."));
            m_pendingPrompts.clear();
            setTurnActive(false);
        });
#ifdef Q_OS_WIN
        m_agent->setCreateProcessArgumentsModifier([](QProcess::CreateProcessArguments *args) {
            constexpr unsigned long kCreateNoWindow = 0x08000000;
            args->flags |= kCreateNoWindow;
        });
#endif
    }

    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    env.insert(QStringLiteral("DLT_AGENT_PORT"), QString::number(m_bridge->port()));
    env.insert(QStringLiteral("DLT_AGENT_TOKEN"), m_bridge->token());
    env.insert(QStringLiteral("PYTHONUNBUFFERED"), QStringLiteral("1"));
    env.insert(QStringLiteral("PYTHONIOENCODING"), QStringLiteral("utf-8"));
    m_agent->setProcessEnvironment(env);
    m_agent->setWorkingDirectory(dir);
    m_agentStderr.clear();
    m_panel->setStatus(tr("Starting agent..."));
    m_agent->start(python, {script});
}

void AiAgentPlugin::stopAgent()
{
    if (!m_agent || m_agent->state() == QProcess::NotRunning)
        return;
    m_bridge->sendEvent(QStringLiteral("shutdown"));
    if (!m_agent->waitForFinished(3000)) {
        m_agent->kill();
        m_agent->waitForFinished(1000);
    }
}

void AiAgentPlugin::flushPendingPrompts()
{
    for (const QString &prompt : std::as_const(m_pendingPrompts))
        m_bridge->sendEvent(QStringLiteral("user_prompt"), {{QStringLiteral("text"), prompt}});
    m_pendingPrompts.clear();
}

void AiAgentPlugin::setTurnActive(bool active)
{
    if (m_panel)
        m_panel->setBusy(active);
}
