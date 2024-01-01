/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { OpenAIChoice } from './OpenAIChoice';

/**
 * Represents a completion response from the OpenAI model.
 *
 * Attributes:
 * id (str): The ID of the completion.
 * object (Literal["completion", "completion.chunk"]): The object type. Defaults to "completion".
 * created (int): The timestamp of the completion.
 * model (Literal["local-gpt"]): The model used to generate the completion. Defaults to "local-gpt".
 * choices (list[OpenAIChoice]): The list of choices made by the model.
 */
export type OpenAICompletion = {
    id: string;
    object?: 'completion' | 'completion.chunk';
    created: number;
    model: any;
    choices: Array<OpenAIChoice>;
};

