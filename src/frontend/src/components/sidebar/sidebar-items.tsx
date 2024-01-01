"use client";

import { AnimatePresence, motion } from "framer-motion";
import { SidebarActions } from "@/components/sidebar/sidebar-actions";
import { SidebarItem } from "@/components/sidebar/sidebar-item";

interface SidebarItemsProps {
  files?: string[];
  refreshFiles: () => Promise<void>;
}

export function SidebarItems({ files, refreshFiles }: SidebarItemsProps) {
  if (!files?.length) return null;

  return (
    <AnimatePresence>
      {files.map(
        (file, index) =>
          file && (
            <motion.div
              key={index}
              exit={{
                opacity: 0,
                height: 0,
              }}
            >
              <SidebarItem index={index} file={file}>
                <SidebarActions file={file} refreshFiles={refreshFiles} />
              </SidebarItem>
            </motion.div>
          )
      )}
    </AnimatePresence>
  );
}
