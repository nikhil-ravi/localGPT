import React from "react";

import { cn } from "@/utils/utils";
import { ExternalLink } from "@/components/external-link";

export function FooterText({ className, ...props }: React.ComponentProps<"p">) {
  return (
    <p
      className={cn(
        "px-2 text-center text-xs leading-normal text-muted-foreground",
        className
      )}
      {...props}
    >
      Open-source, private, context-aware AI chatbot built with{" "}
      <ExternalLink href="https://nextjs.org">Next.js</ExternalLink> and{" "}
      <ExternalLink href="https://www.llamaindex.ai/">LlamaIndex</ExternalLink>.
    </p>
  );
}
