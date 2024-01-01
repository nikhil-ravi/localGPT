import * as React from "react";

import { cn } from "@/utils/utils";
import { buttonVariants } from "@/components/ui/button";
import { IconGitHub, IconSeparator } from "@/components/ui/icons";
import { SidebarMobile } from "./sidebar/sidebar-mobile";
import { SidebarToggle } from "./sidebar/sidebar-toggle";
import { IngestedFiles } from "./ingested-files";

export function Header() {
  return (
    <header className="sticky top-0 z-50 flex items-center justify-between w-full h-16 px-4 border-b shrink-0 bg-gradient-to-b from-background/10 via-background/50 to-background/80 backdrop-blur-xl">
      <div className="flex items-center">
        <React.Suspense fallback={<div className="flex-1 overflow-auto" />}>
          <>
            <SidebarMobile>
              <IngestedFiles />
            </SidebarMobile>
            <SidebarToggle />
          </>
          <div className="flex items-center">
            <IconSeparator className="w-6 h-6 text-muted-foreground/50" />
            <span>LocalGPT</span>
          </div>
        </React.Suspense>
      </div>
      <div className="flex items-center justify-end space-x-2">
        <a
          target="_blank"
          href="https://github.com/nikhil-ravi/localGPT/"
          rel="noopener noreferrer"
          className={cn(buttonVariants({ variant: "outline" }))}
        >
          <IconGitHub />
          <span className="hidden ml-2 md:flex">GitHub</span>
        </a>
      </div>
    </header>
  );
}
