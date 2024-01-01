"use client";

import { cn } from "@/utils/utils";
import { buttonVariants } from "@/components/ui/button";
import { IconPlus } from "@/components/ui/icons";
import { ingest_file } from "@/utils/api-responses";
import toast from "react-hot-toast";
import { ChangeEvent, useRef } from "react";

export type NewDocumentProps = {
  refreshFiles: () => Promise<void>;
};

export function NewDocument({ refreshFiles }: NewDocumentProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleChange = async (
    e: ChangeEvent<HTMLInputElement>
  ): Promise<void> => {
    if (!e.target.files?.length) {
      return;
    }
    const file = e.target.files[0];
    const res = ingest_file(file);

    toast.promise(
      res.then(() => {
        refreshFiles();
      }),
      {
        loading: "Uploading file...",
        success: "File uploaded!",
        error: "Error uploading file.",
      }
    );
  };
  return (
    <div className="px-2 my-4">
      <input
        onChange={handleChange}
        multiple={false}
        ref={fileInputRef}
        type="file"
        hidden
      />
      <button
        onClick={(e) => {
          fileInputRef.current?.click();
        }}
        className={cn(
          buttonVariants({ variant: "outline" }),
          "h-10 w-full justify-start bg-zinc-50 px-4 shadow-none transition-colors hover:bg-zinc-200/40 dark:bg-zinc-900 dark:hover:bg-zinc-300/10"
        )}
      >
        <IconPlus className="-translate-x-2 stroke-2" />
        New Document(s)
      </button>
    </div>
  );
}
