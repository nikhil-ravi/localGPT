import { UseChatHelpers } from "ai/react";

import { Button } from "@/components/ui/button";
import { ExternalLink } from "@/components/external-link";
import { IconArrowRight } from "@/components/ui/icons";

const exampleMessages = [
  {
    heading: "Summarize the document",
    message: `Summarize the following document for a 2nd grader: \n`,
  },
  {
    heading: "Draft an email",
    message: `Draft an email to my boss about the following: \n`,
  },
];

export function EmptyScreen({ setInput }: Pick<UseChatHelpers, "setInput">) {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="rounded-lg border bg-background p-8">
        <h1 className="mb-2 text-lg font-semibold">
          Welcome to the LocalGPT Chatbot!
        </h1>
        <p className="mb-2 leading-normal text-muted-foreground">
          This is an open-source, private, context-aware AI chatbot built with{" "}
          <ExternalLink href="https://nextjs.org">Next.js</ExternalLink>.
        </p>
        <p className="leading-normal text-muted-foreground">
          You can start by adding documents to the chatbot's context and then
          ask it questions about the documents. You can also ask it to explain a
          concept, summarize an article, or draft an email such as:
        </p>
        <div className="mt-4 flex flex-col items-start space-y-2">
          {exampleMessages.map((message, index) => (
            <Button
              key={index}
              variant="link"
              className="h-auto p-0 text-base"
              onClick={() => setInput(message.message)}
            >
              <IconArrowRight className="mr-2 text-muted-foreground" />
              {message.heading}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}
