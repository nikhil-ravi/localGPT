"use client";

import { Suspense, useEffect, useState } from "react";

import { SidebarList } from "@/components/sidebar/sidebar-list";
import { NewDocument } from "./new-document";
import { list_ingested_files } from "@/utils/api-responses";

export function IngestedFiles() {
  const [files, setFiles] = useState<string[]>([]);
  useEffect(() => {
    list_ingested_files().then((files) => setFiles(files));
  }, []);

  const refreshFiles = (): Promise<void> => {
    console.log("Refresh");
    list_ingested_files().then((files) => setFiles(files));
    return Promise.resolve();
  };
  return (
    <div className="flex flex-col h-full">
      <NewDocument refreshFiles={refreshFiles} />
      <Suspense
        fallback={
          <div className="flex flex-col flex-1 px-4 space-y-4 overflow-auto">
            {Array.from({ length: 10 }).map((_, i) => (
              <div
                key={i}
                className="w-full h-6 rounded-md shrink-0 animate-pulse bg-zinc-200 dark:bg-zinc-800"
              />
            ))}
          </div>
        }
      >
        <SidebarList files={files} refreshFiles={refreshFiles} />
      </Suspense>
    </div>
  );
}
