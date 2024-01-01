/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ContextFilter } from './ContextFilter';

/**
 * Represents the body of a request for retrieving chunks of text.
 *
 * Attributes:
 * text (str): The input text.
 * context_filter (ContextFilter | None): The context filter for the text.
 * limit (int): The maximum number of chunks to retrieve.
 * prev_next_chunks (int): The number of previous and next chunks to include.
 */
export type ChunksBody = {
    text: string;
    context_filter?: (ContextFilter | null);
    limit?: number;
    prev_next_chunks?: number;
};

