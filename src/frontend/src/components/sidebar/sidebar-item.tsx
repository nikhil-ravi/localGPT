"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { buttonVariants } from "@/components/ui/button";
import { IconMessage } from "@/components/ui/icons";
import { cn } from "@/utils/utils";

interface SidebarItemProps {
  index: number;
  file: string;
  children: React.ReactNode;
}

export function SidebarItem({ index, file, children }: SidebarItemProps) {
  const shouldAnimate = true;
  return (
    <motion.div
      className="relative h-8"
      variants={{
        initial: {
          height: 0,
          opacity: 0,
        },
        animate: {
          height: "auto",
          opacity: 1,
        },
      }}
      initial={shouldAnimate ? "initial" : undefined}
      animate={shouldAnimate ? "animate" : undefined}
      transition={{
        duration: 0.25,
        ease: "easeIn",
      }}
    >
      <div className="absolute left-2 top-1 flex h-6 w-6 items-center justify-center">
        <IconMessage className="mr-2" />
      </div>
      <div
        className={cn(
          buttonVariants({ variant: "ghost" }),
          "group w-full px-8 transition-colors hover:bg-zinc-200/40 dark:hover:bg-zinc-300/10",
          "bg-zinc-200 pr-16 font-semibold dark:bg-zinc-800"
        )}
      >
        <div
          className="relative max-h-5 flex-1 select-none overflow-hidden text-ellipsis break-all"
          title={file}
        >
          <span className="whitespace-nowrap">
            {shouldAnimate ? (
              file.split("").map((character, index) => (
                <motion.span
                  key={index}
                  variants={{
                    initial: {
                      opacity: 0,
                      x: -100,
                    },
                    animate: {
                      opacity: 1,
                      x: 0,
                    },
                  }}
                  initial={shouldAnimate ? "initial" : undefined}
                  animate={shouldAnimate ? "animate" : undefined}
                  transition={{
                    duration: 0.25,
                    ease: "easeIn",
                    delay: index * 0.05,
                    staggerChildren: 0.05,
                  }}
                >
                  {character}
                </motion.span>
              ))
            ) : (
              <span>{file}</span>
            )}
          </span>
        </div>
      </div>
      {<div className="absolute right-2 top-1">{children}</div>}
    </motion.div>
  );
}
