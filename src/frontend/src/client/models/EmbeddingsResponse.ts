/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { Embedding } from './Embedding';

/**
 * Represents the response object for embeddings.
 *
 * Attributes:
 * object (Literal["list"]): The type of the object, which should always be "list".
 * model (Literal["local-gpt"]): The name of the model, which should always be "local-gpt".
 * data (list[Embedding]): The list of embeddings.
 */
export type EmbeddingsResponse = {
    object: any;
    model: any;
    data: Array<Embedding>;
};

