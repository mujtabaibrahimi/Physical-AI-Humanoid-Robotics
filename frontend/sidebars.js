/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // Main tutorial sidebar with 6 chapters
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'chapter-01',
      label: '1. Introduction to Physical AI',
    },
    {
      type: 'doc',
      id: 'chapter-02',
      label: '2. Basics of Humanoid Robotics',
    },
    {
      type: 'doc',
      id: 'chapter-03',
      label: '3. ROS 2 Fundamentals',
    },
    {
      type: 'doc',
      id: 'chapter-04',
      label: '4. Digital Twin Simulation',
    },
    {
      type: 'doc',
      id: 'chapter-05',
      label: '5. Vision-Language-Action Systems',
    },
    {
      type: 'doc',
      id: 'chapter-06',
      label: '6. Capstone Project',
    },
  ],
};

module.exports = sidebars;
