# RAG_TRANSLATION_POLICY.md

## Purpose

This policy defines the constraints for translating book content
via the integrated RAG chatbot.

Translation is a controlled operation, not a general language service.

---

## Supported Languages

The chatbot may translate retrieved content into:

- English (default)
- Pashto
- Dari

No other languages are permitted.

---

## Translation Scope Rules

- Translation is permitted only on retrieved content.
- Translation must not occur without successful retrieval.
- When user-selected text is provided:
  - Only that text may be translated.
  - Global retrieval is forbidden.

---

## Behavioral Constraints

During translation, the chatbot must:

- Preserve original meaning exactly
- Maintain paragraph and list structure
- Keep technical terms untranslated unless they are standard in target language
- Avoid adding explanations or clarifications

---

## Forbidden Actions

The chatbot must NOT:

- Translate content it did not retrieve
- Infer missing context
- Simplify or summarize content
- Add cultural adaptation or examples

---

## Refusal Behavior

If no relevant content is retrieved, the chatbot must respond with:

> The requested content is not available for translation.

This response is mandatory and unalterable.
