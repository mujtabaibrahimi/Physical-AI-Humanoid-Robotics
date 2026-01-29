import React, { useState, useEffect, useCallback } from 'react';
import styles from './styles.module.css';

/**
 * ReadingProgress - Shows a progress bar indicating how far the user has scrolled
 * through the current page/chapter. Enhances the reading experience by giving
 * users a sense of progress.
 *
 * Features:
 * - Smooth progress bar animation
 * - Respects reduced motion preferences
 * - Only shows on doc pages (not homepage)
 * - Accessible with ARIA attributes
 */
export default function ReadingProgress() {
  const [progress, setProgress] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  const calculateProgress = useCallback(() => {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight;
    const scrollTop = window.scrollY || document.documentElement.scrollTop;

    // Calculate how far we've scrolled as a percentage
    const scrollableHeight = documentHeight - windowHeight;

    if (scrollableHeight <= 0) {
      setProgress(100);
      return;
    }

    const currentProgress = Math.min(
      Math.round((scrollTop / scrollableHeight) * 100),
      100
    );

    setProgress(currentProgress);

    // Show progress bar after user starts scrolling
    setIsVisible(scrollTop > 100);
  }, []);

  useEffect(() => {
    // Check if we're on a doc page (not homepage)
    const isDocPage =
      typeof window !== 'undefined' &&
      (window.location.pathname.includes('/docs/') ||
        window.location.pathname.includes('/chapter'));

    if (!isDocPage) {
      setIsVisible(false);
      return;
    }

    // Initial calculation
    calculateProgress();

    // Throttled scroll handler for performance
    let ticking = false;
    const handleScroll = () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          calculateProgress();
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', calculateProgress, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', calculateProgress);
    };
  }, [calculateProgress]);

  // Don't render if not visible
  if (!isVisible) {
    return null;
  }

  return (
    <div
      className={styles.progressContainer}
      role="progressbar"
      aria-valuenow={progress}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-label={`Reading progress: ${progress}%`}
    >
      <div
        className={styles.progressBar}
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
