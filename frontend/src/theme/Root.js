import React from 'react';
import ReadingProgress from '@site/src/components/ReadingProgress';
import Chatbot from '@site/src/components/Chatbot';

/**
 * Root component wrapper for Docusaurus
 * Used to add global components that should appear on all pages
 */
export default function Root({ children }) {
  return (
    <>
      <ReadingProgress />
      {children}
      <Chatbot />
    </>
  );
}
