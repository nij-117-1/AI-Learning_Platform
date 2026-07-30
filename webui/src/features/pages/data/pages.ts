// src/features/pages/data/pages.ts
/**
 * Static registry of available application pages.
 * Centralized configuration for dashboard navigation cards - edit this file to add/remove pages.
 */

import { Page } from "../types/page";

export const pages: Page[] = [
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