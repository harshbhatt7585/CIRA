import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Phone, Send, ChevronRight } from 'lucide-react';

// Local dev points at the FastAPI server; production uses Vercel's same-origin
// FastAPI function (empty base → relative /api/* calls).
const API_BASE = import.meta.env.VITE_API_BASE ?? (
  import.meta.env.DEV ? `http://${window.location.hostname}:8000` : ''
);

const SUGGESTIONS = [
  { label: '💸  UPI / payment fraud', prompt: 'I lost money through a fraudulent UPI payment.' },
  { label: '📧  Phishing message', prompt: 'I received a phishing email asking for my bank details.' },
  { label: '🔓  Hacked account', prompt: "My social media account has been hacked and I'm locked out." },
  { label: '🚨  Blackmail / sextortion', prompt: 'Someone is threatening to leak my private photos unless I pay.' },
];

// Static first-response steps shown in the left card (mirrors the Streamlit UI).
const EMERGENCY_ACTIONS = [
  { badge: '1930', tone: 'red', title: 'REPORT FRAUD', desc: 'Call the national helpline at 1930 immediately to freeze financial losses.', href: 'tel:1930' },
  { badge: 'NET', tone: 'amber', title: 'GO OFFLINE', desc: 'Disconnect compromised systems or mobile phones from Wi-Fi / Mobile Data.' },
  { badge: 'KEEP', tone: 'blue', title: "DON'T DELETE", desc: 'Preserve all communication logs, chats, SMS alert texts, and transaction screens.' },
  { badge: 'SAFE', tone: 'green', title: 'NEVER SHARE', desc: 'Never share passwords, bank OTPs, or click on files received from unknown actors.' },
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [stage, setStage] = useState('stage_1_intake');
  const [classification, setClassification] = useState(null);
  const [followupAnswers, setFollowupAnswers] = useState({});
  const [summary, setSummary] = useState('');
  const [timeline, setTimeline] = useState([]);
  const [evidence, setEvidence] = useState({});

  const [playbook, setPlaybook] = useState(null);
  const [openSections, setOpenSections] = useState({});

  const [userInput, setUserInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const endRef = useRef(null);
  const inputRef = useRef(null);

  const hasConversation = messages.length > 0;

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Load the playbook whenever the classification changes.
  useEffect(() => {
    if (classification?.subcategory_id) {
      fetch(`${API_BASE}/api/playbook/${classification.subcategory_id}`)
        .then((res) => res.json())
        .then((data) => {
          setPlaybook(data);
          if (data?.available && data.sections) {
            const first = Object.keys(data.sections)[0];
            if (first) setOpenSections({ [first]: true });
          }
        })
        .catch((err) => console.error('Error loading playbook:', err));
    } else {
      setPlaybook(null);
      setOpenSections({});
    }
  }, [classification]);

  const autoGrow = (el) => {
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  };

  const sendMessage = async (text) => {
    const trimmed = (text ?? '').trim();
    if (!trimmed || isLoading) return;

    const priorMessages = messages;
    setMessages([...priorMessages, { role: 'user', content: trimmed, type: 'text' }]);
    setUserInput('');
    if (inputRef.current) inputRef.current.style.height = 'auto';
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: priorMessages,
          stage,
          classification,
          followup_answers: followupAnswers,
          remaining_questions: [],
          evidence,
          user_input: trimmed,
          summary,
          timeline,
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      if (data?.messages) {
        setMessages(data.messages);
        setStage(data.stage || 'stage_1_intake');
        setClassification(data.classification || null);
        setFollowupAnswers(data.followup_answers || {});
        if (data.summary !== undefined) setSummary(data.summary || '');
        if (data.timeline !== undefined) setTimeline(data.timeline || []);
        if (data.evidence !== undefined) setEvidence(data.evidence || {});
      }
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          type: 'text',
          content:
            "I couldn't reach the response service just now. If money was lost, call **1930** immediately and contact your bank. Please try again in a moment.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(userInput);
    }
  };

  const toneClass = (tone) => `ea-badge ea-badge--${tone}`;

  return (
    <div className="cira-root">
      {/* Helpline */}
      <a className="call-1930" href="tel:1930" aria-label="Call cyber fraud helpline 1930">
        <Phone fill="currentColor" />
        <span>Call 1930</span>
      </a>

      {/* Emergency & Action card (left, wide screens) */}
      <aside className="ea-card">
        <p className="ea-card__kicker">Emergency &amp; Action</p>
        <p className="ea-card__title">First response steps</p>
        {EMERGENCY_ACTIONS.map((a) =>
          a.href ? (
            <a className="ea-item" href={a.href} key={a.badge}>
              <span className={toneClass(a.tone)}>{a.badge}</span>
              <span className="ea-body">
                <span className="ea-title">{a.title}</span>
                <span className="ea-desc">{a.desc}</span>
              </span>
            </a>
          ) : (
            <div className="ea-item" key={a.badge}>
              <span className={toneClass(a.tone)}>{a.badge}</span>
              <span className="ea-body">
                <span className="ea-title">{a.title}</span>
                <span className="ea-desc">{a.desc}</span>
              </span>
            </div>
          )
        )}
      </aside>

      <div className="cira-main">
        <h1 className={`cira-heading${hasConversation ? ' cira-heading--compact' : ''}`}>CIRA</h1>

        {!hasConversation && (
          <>
            <p className="cira-tagline">
              Your Cyber Incident Response Assistant. Describe what happened and I'll classify the
              incident, open the right response playbook, and guide your first steps.
            </p>
            <div className="suggestions">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s.label}
                  className="suggestion-chip"
                  onClick={() => sendMessage(s.prompt)}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </>
        )}

        {hasConversation && (
          <div className={`cira-workspace${playbook ? '' : ' cira-workspace--single'}`}>
            <div className="chat-col">
              {messages.map((msg, i) => {
                const isAssistant = msg.role === 'assistant';
                return (
                  <div key={i} className={`msg-row${isAssistant ? '' : ' msg-row--user'}`}>
                    <div className={`avatar avatar--${isAssistant ? 'assistant' : 'user'}`}>
                      {isAssistant ? '🤖' : '🧑'}
                    </div>
                    <div className={`bubble bubble--${isAssistant ? 'assistant' : 'user'}`}>
                      {isAssistant ? (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
                      ) : (
                        msg.content
                      )}
                    </div>
                  </div>
                );
              })}

              {isLoading && (
                <div className="msg-row">
                  <div className="avatar avatar--assistant">🤖</div>
                  <div className="bubble bubble--assistant">
                    <span className="cira-typing" aria-label="Assistant is responding">
                      <span></span>
                      <span></span>
                      <span></span>
                    </span>
                  </div>
                </div>
              )}
              <div ref={endRef} />
            </div>

            {playbook && (
              <aside className="playbook-col">
                <p className="pb-kicker">Active playbook</p>
                <h2 className="pb-title">{classification?.subcategory_name}</h2>
                <p className="pb-meta">
                  {classification?.category_name}
                  {classification?.match_confidence != null &&
                    ` · ${Math.round(classification.match_confidence * 100)}% confidence`}
                </p>

                {playbook.available && playbook.sections ? (
                  Object.entries(playbook.sections).map(([title, content]) => {
                    const isOpen = !!openSections[title];
                    return (
                      <div className="pb-section" key={title}>
                        <button
                          className="pb-section__head"
                          onClick={() =>
                            setOpenSections((prev) => ({ ...prev, [title]: !isOpen }))
                          }
                        >
                          <span>{title}</span>
                          <ChevronRight
                            style={{
                              width: 16,
                              height: 16,
                              transition: 'transform 150ms ease',
                              transform: isOpen ? 'rotate(90deg)' : 'none',
                            }}
                          />
                        </button>
                        {isOpen && (
                          <div className="pb-section__body">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                          </div>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <div className="pb-locked">
                    {playbook.message || 'This playbook is not available yet.'}
                  </div>
                )}
              </aside>
            )}
          </div>
        )}
      </div>

      {/* Docked composer */}
      <div className="composer">
        <div className="composer-inner">
          <div className="composer-shell">
            <textarea
              ref={inputRef}
              className="composer-input"
              rows={1}
              value={userInput}
              placeholder="Message CIRA…"
              disabled={isLoading}
              onChange={(e) => {
                setUserInput(e.target.value);
                autoGrow(e.target);
              }}
              onKeyDown={onKeyDown}
            />
            <button
              className="composer-send"
              onClick={() => sendMessage(userInput)}
              disabled={isLoading || !userInput.trim()}
              aria-label="Send message"
            >
              <Send style={{ width: 18, height: 18 }} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
