/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ContextFilter } from './ContextFilter';

/**
 * Represents the body of a completions request.
 *
 * Attributes:
 * prompt (str): The prompt text.
 * system_prompt (str | None): The system prompt text. Defaults to None.
 * use_context (bool): Flag indicating whether to use context. Defaults to False.
 * context_filter (ContextFilter | None): The context filter. Defaults to None.
 * include_sources (bool): Flag indicating whether to include sources. Defaults to True.
 * stream (bool): Flag indicating whether to stream the response. Defaults to False.
 */
export type CompletionsBody = {
    prompt: string;
    system_prompt?: (string | null);
    use_context?: boolean;
    context_filter?: (ContextFilter | null);
    include_sources?: boolean;
    stream?: boolean;
};

