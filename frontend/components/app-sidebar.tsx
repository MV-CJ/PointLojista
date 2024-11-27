"use client"

import * as React from "react"
import { useTheme } from "next-themes"
import {
  BookOpen,
  Bot,
  Command,
  Frame,
  LifeBuoy,
  Map,
  PieChart,
  Send,
  PencilRuler,
  Settings2,
  SquareTerminal,
  ClipboardList,
  Users,
  Moon,
  Sun,
} from "lucide-react"
import { NavMain } from "@/components/nav-main"
import { NavProjects } from "@/components/nav-projects"
import { NavSecondary } from "@/components/nav-secondary"
import { NavUser } from "@/components/nav-user"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const data = {
  user: {
    name: "B&C Eletrônicos",
    email: "beceletronicos@gmail.com",
    avatar: "/avatars/shadcn.jpg",
  },
  navMain: [
    {
      title: "Orçamentos",
      url: "#",
      icon: ClipboardList,
      isActive: true,
      items: [
        { title: "Novo orçamento", url: "#" },
        { title: "Não pensei", url: "#" },
      ],
    },
    {
      title: "Ordens de Serviço",
      url: "#",
      icon: PencilRuler,
      items: [
        { title: "Nova Ordem de serviço", url: "#" },
        { title: "Não pensei", url: "#" },
        { title: "Não pensei", url: "#" },
      ],
    },
    {
      title: "Atendentes",
      url: "#",
      icon: Users,
      items: [
        { title: "Novo atendente", url: "#" },
        { title: "Não pensei", url: "#" },
        { title: "Não pensei", url: "#" },
        { title: "Não pensei", url: "#" },
      ],
    },
    {
      title: "Configurações",
      url: "#",
      icon: Settings2,
      items: [
        { title: "Minha Loja", url: "#" },
        { title: "Não pensei", url: "#" },
        { title: "Não pensei", url: "#" },
        { title: "Não pensei", url: "#" },
      ],
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { theme, setTheme } = useTheme()

  const navSecondary = [
    {
      title: "Suporte",
      url: "#",
      icon: LifeBuoy,
    },
    {
      title: "Feedback",
      url: "#",
      icon: Send,
    },
    {
      title: theme === "dark" ? "Modo Claro" : "Modo Escuro",
      icon: theme === "dark" ? Sun : Moon,
      onClick: () => setTheme(theme === "dark" ? "light" : "dark"),
      url: "#",
    },
  ]

  return (
    <Sidebar variant="inset" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="flex aspect-square size-8 items-center justify-center">
                  <Command className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">B&C Eletrônicos</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
        {/* Passa o array atualizado com o botão de alternância */}
        <NavSecondary items={navSecondary} className="mt-auto" />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  )
}
