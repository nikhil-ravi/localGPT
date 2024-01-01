/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Chunk } from './Chunk';
import type { OpenAIDelta } from './OpenAIDelta';
import type { OpenAIMessage } from './OpenAIMessage';

/**
 * Represents a choice made by the OpenAI model.
 *
 * Attributes:
 * finish_reason (str, optional): The reason for finishing the choice. Defaults to None.
 * delta (OpenAIDelta, optional): The delta associated with the choice. Defaults to None.
 * message (OpenAIMessage, optional): The message associated with the choice. Defaults to None.
 * sources (list[Chunk], optional): The list of sources associated with the choice. Defaults to None.
 * index (int): The index of the choice.
 */
export type OpenAIChoice = {
    finish_reason: (string | null);
    delta?: (OpenAIDelta | null);
    message?: (OpenAIMessage | null);
    sources?: (Array<Chunk> | null);
    index?: number;
};

