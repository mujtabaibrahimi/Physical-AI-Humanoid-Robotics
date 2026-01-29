import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Learn Physical AI Fundamentals',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
      </svg>
    ),
    description: (
      <>
        Master the core concepts of Physical AI: perception, planning, and control.
        Understand how robots sense and interact with the physical world.
      </>
    ),
  },
  {
    title: 'Hands-On ROS 2 Development',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M9.4 16.6L4.8 12l4.6-4.6L8 6l-6 6 6 6 1.4-1.4zm5.2 0l4.6-4.6-4.6-4.6L16 6l6 6-6 6-1.4-1.4z"/>
      </svg>
    ),
    description: (
      <>
        Build real robotic applications with ROS 2. Learn nodes, topics, services,
        and actions through practical examples and exercises.
      </>
    ),
  },
  {
    title: 'Simulation with Isaac Sim',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zM9 8h2v8H9zm4 0h2v8h-2z"/>
      </svg>
    ),
    description: (
      <>
        Train and test robots in NVIDIA Isaac Sim before deploying to hardware.
        Learn digital twin concepts and sim-to-real transfer.
      </>
    ),
  },
  {
    title: 'Vision-Language-Action Models',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
      </svg>
    ),
    description: (
      <>
        Explore cutting-edge VLA models like RT-2 and OpenVLA. Learn how language
        models ground commands in robotic actions.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2z"/>
      </svg>
    ),
    description: (
      <>
        Study humanoid robot mechanics, locomotion, and manipulation. Understand
        bipedal balance and dexterous hand control.
      </>
    ),
  },
  {
    title: 'Capstone Project',
    Svg: () => (
      <svg viewBox="0 0 24 24" className={styles.featureSvg} aria-hidden="true">
        <path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
      </svg>
    ),
    description: (
      <>
        Apply everything in a comprehensive capstone project. Build an autonomous
        robot system from perception to action.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className={styles.featureCard}>
        <div className={styles.featureIcon}>
          <Svg role="img" />
        </div>
        <div className={styles.featureContent}>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <h2 className={styles.featuresTitle}>What You Will Learn</h2>
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
