"use client";
import { cn } from "@/utils/utils";
import { type Message } from "ai";
import { useChat } from "ai/react";
import { usePathname, useRouter } from "next/navigation";
import React from "react";
import toast from "react-hot-toast";
import { ChatPanel } from "@/components/chat/chat-panel";
import { ChatList } from "@/components/chat/chat-list";
import { ChatScrollAnchor } from "@/components/chat/chat-scroll-anchor";
import { EmptyScreen } from "@/components/chat/empty-screen";

export interface ChatProps extends React.ComponentProps<"div"> {
  id?: string;
  initialMessages?: Message[];
}

export function Chat({ id, initialMessages, className }: ChatProps) {
  const router = useRouter();
  const path = usePathname();
  const { messages, append, reload, stop, isLoading, input, setInput } =
    useChat({
      initialMessages,
      id,
      onResponse(response) {
        if (response.status === 401) toast.error(response.statusText);
      },
      onFinish() {
        if (!path.includes("chat")) {
          router.push(`/chat/${id}`, { scroll: false });
          router.refresh();
        }
      },
    });
  return (
    <>
      <div className={cn("pb-[200px] pt-4 md:pt-10", className)}>
        {messages?.length ? (
          <>
            <ChatList messages={messages} />
            <ChatScrollAnchor trackVisibility={isLoading} />
          </>
        ) : (
          <EmptyScreen setInput={setInput} />
        )}
      </div>
      <ChatPanel
        id={id}
        isLoading={isLoading}
        stop={stop}
        append={append}
        reload={reload}
        messages={messages}
        input={input}
        setInput={setInput}
      />
    </>
  );
}
