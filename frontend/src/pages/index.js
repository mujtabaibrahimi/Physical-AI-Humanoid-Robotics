import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/chapter-01">
            Start Learning
          </Link>
        </div>
      </div>
    </header>
  );
}

function StatsSection() {
  return (
    <section className={styles.statsSection}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>6</div>
            <div className={styles.statLabel}>Chapters</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>50+</div>
            <div className={styles.statLabel}>Code Examples</div>
          </div>
          <div className={styles.statCard}>
            <div className={styles.statNumber}>100%</div>
            <div className={styles.statLabel}>Free Access</div>
          </div>
        </div>
      </div>
    </section>
  );
}

function TechStackSection() {
  const technologies = [
    { name: 'ROS 2', description: 'Robot Operating System' },
    { name: 'Isaac Sim', description: 'NVIDIA Simulation' },
    { name: 'Python', description: 'Primary Language' },
    { name: 'PyTorch', description: 'Deep Learning' },
  ];

  return (
    <section className={styles.techSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Technologies You Will Learn</h2>
        <div className={styles.techGrid}>
          {technologies.map((tech, idx) => (
            <div key={idx} className={styles.techCard}>
              <h3>{tech.name}</h3>
              <p>{tech.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function CTASection() {
  return (
    <section className={styles.ctaSection}>
      <div className="container">
        <h2>Ready to Build Intelligent Robots?</h2>
        <p>Start your journey into Physical AI and Humanoid Robotics today.</p>
        <div className={styles.ctaButtons}>
          <Link
            className="button button--primary button--lg"
            to="/docs/chapter-01">
            Begin Chapter 1
          </Link>
          <Link
            className="button button--outline button--lg"
            to="https://github.com/mujtabaibrahimi/projects">
            View on GitHub
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Interactive textbook for Physical AI and Humanoid Robotics - Learn ROS 2, simulation, and vision-language-action systems">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <StatsSection />
        <TechStackSection />
        <CTASection />
      </main>
    </Layout>
  );
}
