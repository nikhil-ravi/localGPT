/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ContextFilter } from './ContextFilter';
import type { OpenAIMessage } from './OpenAIMessage';

/**
 * Represents the body of a chat request.
 *
 * Attributes:
 * messages (list[OpenAIMessage]): List of messages in the chat.
 * use_context (bool, optional): Flag indicating whether to use context. Defaults to False.
 * context_filter (ContextFilter | None, optional): Context filter. Defaults to None.
 * include_sources (bool, optional): Flag indicating whether to include sources. Defaults to True.
 * stream (bool, optional): Flag indicating whether to stream the chat. Defaults to False.
 */
export type ChatBody = {
    messages: Array<OpenAIMessage>;
    use_context?: boolean;
    context_filter?: (ContextFilter | null);
    include_sources?: boolean;
    stream?: boolean;
};

