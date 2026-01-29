import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

const API_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-backend-url.railway.app/api'
  : 'http://localhost:8000/api';

// Policy-mandated refusal messages
const REFUSAL_NO_CONTENT = "The answer is not available in the selected content.";
const REFUSAL_NO_TRANSLATION = "The requested content is not available for translation.";

// Supported languages per RAG_TRANSLATION_POLICY.md
const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'pashto', label: 'Pashto' },
  { code: 'dari', label: 'Dari' }
];

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I can help you understand concepts from this Physical AI textbook. Ask me anything about robotics, AI, or select text from the book to ask about specific content.',
      canTranslate: false
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [targetLanguage, setTargetLanguage] = useState('en');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Listen for text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim();

      // Only capture selection from doc content area
      if (text && text.length > 10 && text.length < 2000) {
        const anchorNode = selection.anchorNode;
        const isInDocContent = anchorNode?.parentElement?.closest('.markdown, article, .theme-doc-markdown');

        if (isInDocContent) {
          setSelectedText(text);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    const currentSelectedText = selectedText;

    setInput('');
    setSelectedText(''); // Clear selection after use

    // Add user message with context indicator
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      hasSelection: !!currentSelectedText,
      selectionPreview: currentSelectedText ? currentSelectedText.slice(0, 100) + '...' : null
    }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMessage,
          selected_text: currentSelectedText || undefined
        }),
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        grounded: data.grounded,
        canTranslate: data.grounded && data.response !== REFUSAL_NO_CONTENT,
        originalContent: data.response
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. The backend service may be unavailable. Please try again later.',
        canTranslate: false
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslate = async (messageIndex) => {
    if (targetLanguage === 'en') return;

    const message = messages[messageIndex];
    if (!message.canTranslate || !message.originalContent) return;

    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content: message.originalContent,
          target_language: targetLanguage
        }),
      });

      if (!response.ok) throw new Error('Translation failed');

      const data = await response.json();

      if (data.translated === REFUSAL_NO_TRANSLATION) {
        // Translation refused per policy
        return;
      }

      // Update the message with translation
      setMessages(prev => prev.map((msg, idx) =>
        idx === messageIndex
          ? {
              ...msg,
              content: data.translated,
              isTranslated: true,
              translatedLanguage: targetLanguage
            }
          : msg
      ));
    } catch (error) {
      console.error('Translation error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleShowOriginal = (messageIndex) => {
    setMessages(prev => prev.map((msg, idx) =>
      idx === messageIndex
        ? {
            ...msg,
            content: msg.originalContent,
            isTranslated: false,
            translatedLanguage: null
          }
        : msg
    ));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const clearSelection = () => {
    setSelectedText('');
    window.getSelection()?.removeAllRanges();
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <button
        className={styles.chatToggle}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chat' : 'Open chat assistant'}
        aria-expanded={isOpen}
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
            <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
            <path fill="currentColor" d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
          </svg>
        )}
      </button>

      {/* Chat Modal */}
      {isOpen && (
        <div
          className={styles.chatModal}
          role="dialog"
          aria-label="Chat with AI assistant"
          onKeyDown={handleKeyDown}
        >
          <div className={styles.chatHeader}>
            <div className={styles.headerTop}>
              <h3>AI Assistant</h3>
              <select
                className={styles.languageSelect}
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                aria-label="Select language for translation"
              >
                {LANGUAGES.map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.label}
                  </option>
                ))}
              </select>
            </div>
            <span className={styles.chatSubtitle}>
              {selectedText ? 'Text selected - ask about it' : 'Ask about Physical AI concepts'}
            </span>
          </div>

          {/* Selected Text Indicator */}
          {selectedText && (
            <div className={styles.selectionBanner}>
              <span className={styles.selectionIcon}>
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="currentColor" d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </span>
              <span className={styles.selectionText}>
                "{selectedText.slice(0, 50)}{selectedText.length > 50 ? '...' : ''}"
              </span>
              <button
                className={styles.clearSelection}
                onClick={clearSelection}
                aria-label="Clear selection"
              >
                <svg viewBox="0 0 24 24" width="14" height="14">
                  <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
              </button>
            </div>
          )}

          <div className={styles.chatMessages} role="log" aria-live="polite">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`${styles.message} ${styles[msg.role]}`}
              >
                <div className={styles.messageContent}>
                  {msg.hasSelection && msg.selectionPreview && (
                    <div className={styles.queryContext}>
                      <small>Regarding: "{msg.selectionPreview}"</small>
                    </div>
                  )}
                  {msg.content}

                  {/* Translation controls for assistant messages */}
                  {msg.role === 'assistant' && msg.canTranslate && targetLanguage !== 'en' && (
                    <div className={styles.translateControls}>
                      {msg.isTranslated ? (
                        <button
                          className={styles.translateBtn}
                          onClick={() => handleShowOriginal(idx)}
                        >
                          Show Original
                        </button>
                      ) : (
                        <button
                          className={styles.translateBtn}
                          onClick={() => handleTranslate(idx)}
                          disabled={isLoading}
                        >
                          Translate to {LANGUAGES.find(l => l.code === targetLanguage)?.label}
                        </button>
                      )}
                    </div>
                  )}

                  {msg.isTranslated && (
                    <div className={styles.translatedBadge}>
                      Translated to {LANGUAGES.find(l => l.code === msg.translatedLanguage)?.label}
                    </div>
                  )}

                  {msg.sources && msg.sources.length > 0 && (
                    <div className={styles.sources}>
                      <span>Sources: </span>
                      {msg.sources.map((src, i) => (
                        <a key={i} href={`/docs/${src}`}>{src}</a>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.typing}>
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className={styles.chatForm} onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={selectedText ? "Ask about selected text..." : "Ask a question..."}
              disabled={isLoading}
              aria-label="Type your message"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              aria-label="Send message"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
              </svg>
            </button>
          </form>
        </div>
      )}
    </>
  );
}
