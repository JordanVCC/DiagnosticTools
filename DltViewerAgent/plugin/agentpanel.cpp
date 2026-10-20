#include "agentpanel.h"

#include <QHBoxLayout>
#include <QKeyEvent>
#include <QLabel>
#include <QPlainTextEdit>
#include <QPushButton>
#include <QScrollBar>
#include <QTextBrowser>
#include <QTimer>
#include <QUrl>
#include <QVBoxLayout>

AgentPanel::AgentPanel(QWidget *parent)
    : QWidget(parent),
      m_transcript(new QTextBrowser(this)),
      m_input(new QPlainTextEdit(this)),
      m_send(new QPushButton(tr("Send"), this)),
      m_stop(new QPushButton(tr("Stop"), this)),
      m_newChat(new QPushButton(tr("New chat"), this)),
      m_status(new QLabel(this)),
      m_selected(new QLabel(this)),
      m_renderTimer(new QTimer(this))
{
    m_transcript->setOpenLinks(false);
    m_transcript->setPlaceholderText(tr("Ask about the open log, e.g. \"Summarise the errors\" or \"Explain the selected message\"."));
    m_input->setPlaceholderText(tr("Message the agent (Enter to send, Shift+Enter for a new line)"));
    m_input->setMaximumHeight(90);
    m_input->installEventFilter(this);
    m_status->setWordWrap(true);
    m_stop->setEnabled(false);

    m_renderTimer->setSingleShot(true);
    m_renderTimer->setInterval(80);
    connect(m_renderTimer, &QTimer::timeout, this, &AgentPanel::render);

    auto *buttons = new QHBoxLayout;
    buttons->addWidget(m_selected, 1);
    buttons->addWidget(m_newChat);
    buttons->addWidget(m_stop);
    buttons->addWidget(m_send);

    auto *layout = new QVBoxLayout(this);
    layout->addWidget(m_status);
    layout->addWidget(m_transcript, 1);
    layout->addWidget(m_input);
    layout->addLayout(buttons);

    connect(m_send, &QPushButton::clicked, this, &AgentPanel::submit);
    connect(m_stop, &QPushButton::clicked, this, &AgentPanel::stopRequested);
    connect(m_newChat, &QPushButton::clicked, this, &AgentPanel::newChatRequested);
    connect(m_transcript, &QTextBrowser::anchorClicked, this, [this](const QUrl &url) {
        bool ok = false;
        const int index = url.host().isEmpty() ? url.path().toInt(&ok) : url.host().toInt(&ok);
        if (url.scheme() == QLatin1String("dlt") && ok)
            emit jumpRequested(index);
    });

    setSelectedIndex(-1);
}

void AgentPanel::appendUser(const QString &text)
{
    m_entries.append({Role::User, text});
    scheduleRender();
}

void AgentPanel::appendAssistantDelta(const QString &text)
{
    if (m_entries.isEmpty() || m_entries.last().role != Role::Assistant)
        m_entries.append({Role::Assistant, QString()});
    m_entries.last().text += text;
    scheduleRender();
}

void AgentPanel::setAssistantMessage(const QString &text)
{
    if (text.trimmed().isEmpty())
        return;
    if (m_entries.isEmpty() || m_entries.last().role != Role::Assistant)
        m_entries.append({Role::Assistant, QString()});
    m_entries.last().text = text;
    scheduleRender();
}

void AgentPanel::appendTool(const QString &text)
{
    m_entries.append({Role::Tool, text});
    scheduleRender();
}

void AgentPanel::appendError(const QString &text)
{
    m_entries.append({Role::Error, text});
    scheduleRender();
}

void AgentPanel::setStatus(const QString &text) { m_status->setText(text); }

void AgentPanel::setSelectedIndex(int index)
{
    m_selected->setText(index < 0 ? tr("No message selected") : tr("Selected: #%1").arg(index));
}

void AgentPanel::setBusy(bool busy)
{
    m_busy = busy;
    m_send->setEnabled(!busy);
    m_stop->setEnabled(busy);
}

void AgentPanel::clearTranscript()
{
    m_entries.clear();
    render();
}

bool AgentPanel::eventFilter(QObject *watched, QEvent *event)
{
    if (watched == m_input && event->type() == QEvent::KeyPress) {
        const auto *key = static_cast<QKeyEvent *>(event);
        if ((key->key() == Qt::Key_Return || key->key() == Qt::Key_Enter) && !(key->modifiers() & Qt::ShiftModifier)) {
            submit();
            return true;
        }
    }
    return QWidget::eventFilter(watched, event);
}

void AgentPanel::submit()
{
    const QString text = m_input->toPlainText().trimmed();
    if (text.isEmpty() || m_busy)
        return;
    m_input->clear();
    emit promptSubmitted(text);
}

void AgentPanel::scheduleRender()
{
    if (!m_renderTimer->isActive())
        m_renderTimer->start();
}

void AgentPanel::render()
{
    QScrollBar *bar = m_transcript->verticalScrollBar();
    const bool atBottom = bar->value() >= bar->maximum() - 4;

    QString markdown;
    for (const Entry &entry : std::as_const(m_entries)) {
        switch (entry.role) {
        case Role::User:
            markdown += QStringLiteral("**You:** ") + entry.text.toHtmlEscaped() + QStringLiteral("\n\n");
            break;
        case Role::Assistant:
            markdown += entry.text + QStringLiteral("\n\n");
            break;
        case Role::Tool:
            markdown += QStringLiteral("*") + entry.text.toHtmlEscaped() + QStringLiteral("*\n\n");
            break;
        case Role::Error:
            markdown += QStringLiteral("**Error:** ") + entry.text.toHtmlEscaped() + QStringLiteral("\n\n");
            break;
        }
        markdown += QStringLiteral("---\n\n");
    }
    m_transcript->setMarkdown(markdown);
    if (atBottom)
        bar->setValue(bar->maximum());
}
