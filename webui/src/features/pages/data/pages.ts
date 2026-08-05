// src/features/pages/data/pages.ts
/**
 * Static registry of available application pages.
 * Centralized configuration for dashboard navigation cards - edit this file to add/remove pages.
 */

import { Page } from "../types/page";

export const pages: Page[] = [
  {
    id: "linguistic",
    title: "Linguistic Hub",
    description: "AI-powered language tools: idiomatic expressions with meaning, cultural context, and real-world usage.",
    href: "/linguistic",
    category: "Education",
    tags: ["linguistic", "language", "idioms", "learning", "education"]
  },
  {
    id: "idioms",
    title: "Idioms",
    description: "Learn an idiomatic expression in a target language with meaning, pronunciation, and a dialogue.",
    href: "/linguistic/idioms",
    category: "Education",
    tags: ["linguistic", "idioms", "language", "expressions", "education"]
  },
  {
    id: "word-of-the-day",
    title: "Word of the Day",
    description: "Discover a rich word from a target language with pronunciation, morphology, and history.",
    href: "/linguistic/word-of-the-day",
    category: "Education",
    tags: ["linguistic", "word", "language", "vocabulary", "education"]
  },
  {
    id: "translator",
    title: "Translator",
    description: "Contextual translation with a chosen tone, reference material, and cultural notes.",
    href: "/linguistic/translator",
    category: "Education",
    tags: ["linguistic", "translator", "translation", "language", "education"]
  },
  {
    id: "simulator",
    title: "Simulator",
    description: "Behavioral simulations: put a persona in a scenario, deliver your line, and see how they think, act, and reply.",
    href: "/linguistic/simulator",
    category: "Education",
    tags: ["linguistic", "simulator", "roleplay", "conversation", "education"]
  },
  {
    id: "sentence-of-the-day",
    title: "Sentence of the Day",
    description: "Discover the daily featured sentence in a target language with grammar, culture, and variations.",
    href: "/linguistic/sentence-of-the-day",
    category: "Education",
    tags: ["linguistic", "sentence", "language", "grammar", "education"]
  },
  {
    id: "rewriter",
    title: "Rewriter",
    description: "Rewrite text to improve quality, adjust tone, or change structure while preserving the original intent.",
    href: "/linguistic/rewriter",
    category: "Education",
    tags: ["linguistic", "rewriter", "writing", "language", "education"]
  },
  {
    id: "lesson",
    title: "Language Lesson",
    description: "Generate a scaffolded language lesson tuned to your CEFR level, learning focus, and theme.",
    href: "/linguistic/lesson",
    category: "Education",
    tags: ["linguistic", "lesson", "language", "learning", "education"]
  },
  {
    id: "poet-engine",
    title: "Poet Engine",
    description: "Explain the 'Soul' of a word using AI-driven poetic philology — etymology, poetry, and metaphor.",
    href: "/linguistic/poet-engine",
    category: "Education",
    tags: ["linguistic", "poetry", "language", "words", "education"]
  },
  {
    id: "language-tester",
    title: "Language Tester",
    description: "Generate personalized MCQs, fill-in-the-blank, translation challenges, and coached roleplays at your CEFR level.",
    href: "/linguistic/language-tester",
    category: "Education",
    tags: ["linguistic", "assessment", "language", "quiz", "education"]
  },
  {
    id: "roleplay",
    title: "Roleplay",
    description: "Step into a scene with any persona you describe and hold an in-character conversation.",
    href: "/linguistic/roleplay",
    category: "Education",
    tags: ["linguistic", "roleplay", "conversation", "language", "education"]
  },
  {
    id: "learning",
    title: "Learning Hub",
    description: "AI-powered explainer tools: quick explanations, A-to-Z tutorials, Feynman simplifications, and more.",
    href: "/learning",
    category: "Education",
    tags: ["learning", "explainer", "tutorial", "study", "education"]
  },
  {
    id: "roadmap",
    title: "Roadmap Planner",
    description: "Generate AI-powered learning roadmaps with main points, subpoints, milestones, and progress tracking.",
    href: "/learning/roadmap",
    category: "Education",
    tags: ["roadmap", "learning", "planner", "study", "education"]
  },
  {
    id: "guides",
    title: "Learning Guides",
    description: "Guided tasks, daily study plans, project blueprints, and topic and project suggestions powered by AI.",
    href: "/learning/guides",
    category: "Education",
    tags: ["learning", "guides", "tasks", "planner", "education"]
  },
  {
    id: "memory-helper",
    title: "Memory Mnemonics",
    description: "Transform complex data into structured mnemonics and a spaced retention plan.",
    href: "/learning/memory-helper",
    category: "Education",
    tags: ["learning", "memory", "mnemonics", "study", "education"]
  },
  {
    id: "motivation",
    title: "Motivation & Reflection",
    description: "Personalized motivational quotes and deep journaling prompts tuned to your emotional state.",
    href: "/learning/motivation",
    category: "Education",
    tags: ["learning", "motivation", "reflection", "journal", "education"]
  },
  {
    id: "projects",
    title: "Project Recommender",
    description: "Hands-on project ideas matched to your topic, scope, and difficulty level.",
    href: "/learning/projects",
    category: "Education",
    tags: ["learning", "projects", "practice", "build", "education"]
  },
  {
    id: "skill-architect",
    title: "Skill Architect",
    description: "Deconstruct a domain into its root skills and a level-wise progression tree with proof of mastery.",
    href: "/learning/skill-architect",
    category: "Education",
    tags: ["learning", "skills", "architecture", "progression", "education"]
  },
  {
    id: "tutor",
    title: "Adaptive Tutor",
    description: "Personalized explanations adapted to your level, learning style, and current scenario.",
    href: "/learning/tutor",
    category: "Education",
    tags: ["learning", "tutor", "adaptive", "explanation", "education"]
  },
  {
    id: "tutor-chat",
    title: "Tutor Chat",
    description: "A topic-scoped tutor chatbot that explains concepts and breaks them down each turn.",
    href: "/learning/tutor-chat",
    category: "Education",
    tags: ["learning", "chatbot", "tutor", "conversation", "education"]
  },
  {
    id: "analytics",
    title: "Analytics Dashboard",
    description: "View comprehensive metrics, user engagement statistics, and performance indicators.",
    href: "/dashboard/analytics",
    category: "Analytics",
    tags: ["metrics", "charts", "reports", "statistics", "graphs"]
  },
  {
    id: "users",
    title: "User Management",
    description: "Manage user accounts, roles, permissions, and access control settings.",
    href: "/dashboard/users",
    category: "Management",
    tags: ["users", "permissions", "admin", "accounts", "roles"]
  },
  {
    id: "settings",
    title: "System Settings",
    description: "Configure application preferences, integrations, and global system configurations.",
    href: "/dashboard/settings",
    category: "Configuration",
    tags: ["config", "preferences", "system", "setup", "options"]
  },
  {
    id: "billing",
    title: "Billing & Subscription",
    description: "Manage payment methods, view invoices, and upgrade subscription plans.",
    href: "/dashboard/billing",
    category: "Finance",
    tags: ["payments", "invoices", "subscription", "pricing", "billing"]
  },
  {
    id: "content",
    title: "Content Manager",
    description: "Create, edit, and publish content across your application and marketing channels.",
    href: "/dashboard/content",
    category: "Content",
    tags: ["cms", "posts", "articles", "media", "blog"]
  },
  {
    id: "api-keys",
    title: "API Keys",
    description: "Generate and manage API keys for third-party integrations and developer access.",
    href: "/dashboard/api-keys",
    category: "Development",
    tags: ["api", "keys", "integration", "developers", "webhooks"]
  },
  {
    id: "security",
    title: "Security Center",
    description: "Monitor security logs, configure 2FA, and manage audit trails.",
    href: "/dashboard/security",
    category: "Security",
    tags: ["logs", "audit", "2fa", "protection", "privacy"]
  },
  {
    id: "admin",
    title: "Admin Panel",
    description: "Manage users, pages, billing, and system settings.",
    href: "/admin",
    category: "Administration",
    tags: ["admin", "management", "settings", "users", "configuration"]
  }
];