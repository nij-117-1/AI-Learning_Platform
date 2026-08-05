// src/features/practice/components/PracticeSidebar.tsx
/**
 * Left navigation for the Practice area. Lists the Testing Portal and
 * Performance Grader from their registries and highlights the active route.
 * Collapses to an icon rail on desktop and a drawer on mobile via the shadcn
 * Sidebar primitives.
 */
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Dumbbell } from "lucide-react";
import type { LearningTool } from "@/features/learning/lib/learning-tools";
import { testingPortalTools } from "@/features/practice/lib/testing-portal-tools";
import { graderTools } from "@/features/practice/lib/grader-tools";

function ToolGroup({ label, tools, pathname }: { label: string; tools: LearningTool[]; pathname: string }) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>{label}</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenu>
          {tools.map((tool) => (
            <SidebarMenuItem key={tool.id}>
              <SidebarMenuButton asChild isActive={pathname === tool.href} tooltip={tool.shortTitle}>
                <Link href={tool.href}>
                  <tool.icon />
                  <span>{tool.shortTitle}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}

export function PracticeSidebar() {
  const pathname = usePathname();

  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-1">
          <div className="flex min-w-0 flex-1 items-center gap-2">
            <Dumbbell className="h-5 w-5 shrink-0 text-primary" />
            <span className="group-data-[collapsible=icon]:hidden truncate text-sm font-semibold">
              Practice Hub
            </span>
          </div>
          <SidebarTrigger className="group-data-[collapsible=icon]:hidden" />
        </div>
      </SidebarHeader>
      <SidebarSeparator />
      <SidebarContent>
        <ToolGroup label="Assessment" tools={testingPortalTools} pathname={pathname} />
        <ToolGroup label="Feedback" tools={graderTools} pathname={pathname} />
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}
