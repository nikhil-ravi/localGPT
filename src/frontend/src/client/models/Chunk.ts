/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngestedDoc } from './IngestedDoc';

/**
 * Represents a chunk of text.
 *
 * Attributes:
 * object (Literal["context.chunk"]): The object type of the chunk.
 * score (float): The score of the chunk.
 * document (IngestedDoc): The ingested document associated with the chunk.
 * text (str): The text content of the chunk.
 * previous_texts (list[str] | None): The list of previous texts, if any.
 * next_texts (list[str] | None): The list of next texts, if any.
 */
export type Chunk = {
    object: any;
    score: number;
    document: IngestedDoc;
    text: string;
    previous_texts?: (Array<string> | null);
    next_texts?: (Array<string> | null);
};

