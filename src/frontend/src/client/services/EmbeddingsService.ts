/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { EmbeddingsBody } from '../models/EmbeddingsBody';
import type { EmbeddingsResponse } from '../models/EmbeddingsResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class EmbeddingsService {

    /**
     * Embeddings Generation
     * Get a vector representation of a given input.
     *
     * That vector representation can be easily consumed by machine learning models and algorithms.
     *
     * Args:
     * request (Request): The HTTP request object.
     * body (EmbeddingsBody): The request body containing the input texts.
     *
     * Returns:
     * EmbeddingsResponse: The response object containing the generated embeddings.
     * @returns EmbeddingsResponse Successful Response
     * @throws ApiError
     */
    public static embeddingsGenerationApiEmbeddingsPost({
        requestBody,
    }: {
        requestBody: EmbeddingsBody,
    }): CancelablePromise<EmbeddingsResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/embeddings',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
