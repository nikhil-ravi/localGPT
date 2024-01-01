/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChunksBody } from '../models/ChunksBody';
import type { ChunksResponse } from '../models/ChunksResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ContextChunksService {

    /**
     * Chunks Retrieval
     * Given a `text`, returns the most relevant chunks from the ingested documents.
     *
     * The returned information can be used to generate prompts that can be
     * passed to `/completions` or `/chat/completions` APIs. Note: it is usually a very fast API, because only the Embeddings model is involved, not the LLM. The returned information contains the relevant chunk `text` together with the source `document` it is coming from. It also contains a score that can be used to compare different results.
     *
     * The max number of chunks to be returned is set using the `limit` param.
     *
     * Previous and next chunks (pieces of text that appear right before or after in the document) can be fetched by using the `prev_next_chunks` field.
     *
     * The documents being used can be filtered using the `context_filter` and passing the document IDs to be used. Ingested documents IDs can be found using `/ingest/list` endpoint. If you want all ingested documents to be used, remove `context_filter` altogether.
     *
     * Args:
     * request (Request): The incoming request object.
     * body (ChunksBody): The request body containing the text and context filter.
     *
     * Returns:
     * ChunksResponse: The response object containing the retrieved chunks.
     * @returns ChunksResponse Successful Response
     * @throws ApiError
     */
    public static chunksRetrievalApiChunksPost({
        requestBody,
    }: {
        requestBody: ChunksBody,
    }): CancelablePromise<ChunksResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/chunks',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
