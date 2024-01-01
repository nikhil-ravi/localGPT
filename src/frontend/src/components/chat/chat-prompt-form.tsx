import { useRef, useEffect, ChangeEvent } from "react";
import Textarea from "react-textarea-autosize";
import { UseChatHelpers } from "ai/react";
import { useEnterSubmit } from "@/hooks/use-enter-submit";
import { cn } from "@/utils/utils";
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { IconArrowElbow, IconPlus } from "@/components/ui/icons";
import toast from "react-hot-toast";
import { ingest_file } from "@/utils/api-responses";

export interface PromptProps
  extends Pick<UseChatHelpers, "input" | "setInput"> {
  onSubmit: (value: string) => void;
  isLoading: boolean;
}

export function PromptForm({
  onSubmit,
  input,
  setInput,
  isLoading,
}: PromptProps) {
  const { formRef, onKeyDown } = useEnterSubmit();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const handleChange = async (
    e: ChangeEvent<HTMLInputElement>
  ): Promise<void> => {
    if (!e.target.files?.length) {
      return;
    }
    const file = e.target.files[0];
    const res = ingest_file(file);

    toast.promise(res, {
      loading: "Uploading file...",
      success: "File uploaded!",
      error: "Error uploading file.",
    });
  };

  return (
    <form
      onSubmit={async (e) => {
        e.preventDefault();
        if (!input?.trim()) {
          return;
        }
        setInput("");
        await onSubmit(input);
      }}
      ref={formRef}
    >
      <div className="relative flex flex-col w-full px-8 overflow-hidden max-h-60 grow bg-background sm:rounded-md sm:border sm:px-12">
        <input
          onChange={handleChange}
          multiple={false}
          ref={fileInputRef}
          type="file"
          hidden
        />
        <Tooltip>
          <TooltipTrigger asChild>
            <button
              onClick={(e) => {
                fileInputRef.current?.click();
              }}
              className={cn(
                buttonVariants({ size: "sm", variant: "outline" }),
                "absolute left-0 top-4 h-8 w-8 rounded-full bg-background p-0 sm:left-4"
              )}
            >
              <IconPlus />
              <span className="sr-only">Add Document(s)</span>
            </button>
          </TooltipTrigger>
          <TooltipContent>Add Document(s)</TooltipContent>
        </Tooltip>
        <Textarea
          ref={inputRef}
          tabIndex={0}
          onKeyDown={onKeyDown}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Send a message."
          spellCheck={false}
          className="min-h-[60px] w-full resize-none bg-transparent px-4 py-[1.3rem] focus-within:outline-none sm:text-sm"
        />
        <div className="absolute right-0 top-4 sm:right-4">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                type="submit"
                size="icon"
                disabled={isLoading || input === ""}
              >
                <IconArrowElbow />
                <span className="sr-only">Send message</span>
              </Button>
            </TooltipTrigger>
            <TooltipContent>Send message</TooltipContent>
          </Tooltip>
        </div>
      </div>
    </form>
  );
}
