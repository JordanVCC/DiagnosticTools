#ifndef AGENTPANEL_H
#define AGENTPANEL_H

#include <QList>
#include <QWidget>

class QLabel;
class QPlainTextEdit;
class QPushButton;
class QTextBrowser;
class QTimer;

// Docked chat UI. Message references written as dlt://<index> links emit jumpRequested().
class AgentPanel : public QWidget
{
    Q_OBJECT

public:
    explicit AgentPanel(QWidget *parent = nullptr);

    void appendUser(const QString &text);
    void appendAssistantDelta(const QString &text);
    void setAssistantMessage(const QString &text);
    void appendTool(const QString &text);
    void appendError(const QString &text);
    void setStatus(const QString &text);
    void setSelectedIndex(int index);
    void setBusy(bool busy);
    void clearTranscript();

signals:
    void promptSubmitted(const QString &text);
    void stopRequested();
    void newChatRequested();
    void jumpRequested(int index);

protected:
    bool eventFilter(QObject *watched, QEvent *event) override;

private:
    enum class Role { User, Assistant, Tool, Error };
    struct Entry { Role role; QString text; };

    void submit();
    void scheduleRender();
    void render();

    QTextBrowser *m_transcript;
    QPlainTextEdit *m_input;
    QPushButton *m_send;
    QPushButton *m_stop;
    QPushButton *m_newChat;
    QLabel *m_status;
    QLabel *m_selected;
    QTimer *m_renderTimer;
    QList<Entry> m_entries;
    bool m_busy = false;
};

#endif // AGENTPANEL_H
