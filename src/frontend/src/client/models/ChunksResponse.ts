/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Chunk } from './Chunk';

/**
 * Represents the response for chunks.
 *
 * Attributes:
 * object (Literal["list"]): The type of object returned, which is always "list".
 * model (Literal["local-gpt"]): The model used for generating the chunks, which is always "local-gpt".
 * data (list[Chunk]): The list of chunks.
 */
export type ChunksResponse = {
    object: any;
    model: any;
    data: Array<Chunk>;
};

