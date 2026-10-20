#ifndef AIAGENTPLUGIN_H
#define AIAGENTPLUGIN_H

#include <QObject>
#include <QPointer>
#include <QProcess>
#include <QStringList>

#include "plugininterface.h"

#define AI_AGENT_PLUGIN_VERSION "0.1.0"

class AgentBridge;
class AgentPanel;

class AiAgentPlugin : public QObject, QDLTPluginInterface, QDltPluginViewerInterface, QDltPluginControlInterface
{
    Q_OBJECT
    Q_INTERFACES(QDLTPluginInterface)
    Q_INTERFACES(QDltPluginViewerInterface)
    Q_INTERFACES(QDltPluginControlInterface)
    Q_PLUGIN_METADATA(IID "org.diagnostictools.DLT.AiAgentPlugin")

public:
    AiAgentPlugin();
    ~AiAgentPlugin() override;

    /* QDLTPluginInterface */
    QString name() override;
    QString pluginVersion() override;
    QString pluginInterfaceVersion() override;
    QString description() override;
    QString error() override;
    bool loadConfig(QString filename) override;
    bool saveConfig(QString filename) override;
    QStringList infoConfig() override;

    /* QDltPluginViewerInterface */
    QWidget *initViewer() override;
    void initFileStart(QDltFile *file) override;
    void initFileFinish() override;
    void initMsg(int index, QDltMsg &msg) override;
    void initMsgDecoded(int index, QDltMsg &msg) override;
    void updateFileStart() override;
    void updateMsg(int index, QDltMsg &msg) override;
    void updateMsgDecoded(int index, QDltMsg &msg) override;
    void updateFileFinish() override;
    void selectedIdxMsg(int index, QDltMsg &msg) override;
    void selectedIdxMsgDecoded(int index, QDltMsg &msg) override;

    /* QDltPluginControlInterface */
    bool initControl(QDltControl *control) override;
    bool initConnections(QStringList list) override;
    bool controlMsg(int index, QDltMsg &msg) override;
    bool stateChanged(int index, QDltConnection::QDltConnectionState connectionState, QString hostname) override;
    bool autoscrollStateChanged(bool enabled) override;
    void initMessageDecoder(QDltMessageDecoder *messageDecoder) override;
    void initMainTableView(QTableView *pTableView) override;
    void configurationChanged() override;

private:
    void onPrompt(const QString &text);
    void onAgentEvent(const QString &name, const QJsonObject &data);
    void startAgent();
    void stopAgent();
    void flushPendingPrompts();
    void setTurnActive(bool active);

    AgentBridge *m_bridge = nullptr;
    QPointer<AgentPanel> m_panel;
    QProcess *m_agent = nullptr;
    QDltFile *m_file = nullptr;
    QStringList m_pendingPrompts;
    QByteArray m_agentStderr;
    QString m_error;
};

#endif // AIAGENTPLUGIN_H
