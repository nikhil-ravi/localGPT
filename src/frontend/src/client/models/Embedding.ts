/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Represents an embedding object.
 *
 * Attributes:
 * index (int): The index of the embedding.
 * object (Literal["embedding"]): The type of object, which should always be "embedding".
 * embedding (list[float]): The embedding values.
 */
export type Embedding = {
    index: number;
    object: any;
    embedding: Array<number>;
};

