/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ChatBody } from '../models/ChatBody';
import type { CompletionsBody } from '../models/CompletionsBody';
import type { OpenAICompletion } from '../models/OpenAICompletion';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ContextualCompletionsService {

    /**
     * Chat Completion
     * Handles the chat completion API endpoint.
     *
     * Args:
     * request (Request): The FastAPI request object.
     * body (ChatBody): The request body containing chat messages and configuration.
     *
     * Returns:
     * Union[OpenAICompletion, StreamingResponse]: The completion response or a streaming response.
     * @returns OpenAICompletion Successful Response
     * @throws ApiError
     */
    public static chatCompletionApiChatCompletionsPost({
        requestBody,
    }: {
        requestBody: ChatBody,
    }): CancelablePromise<OpenAICompletion> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/chat/completions',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Completion
     * We recommend most users use our Chat completions API.
     *
     * Given a prompt, the model will return one predicted completion.
     *
     * Optionally include a `system_prompt` to influence the way the LLM answers.
     *
     * If `use_context` is set to `true`, the model will use context coming  from the ingested documents to create the response. The documents being used can be filtered using the `context_filter` and passing the document IDs to be used. Ingested documents IDs can be found using `/ingest/list` endpoint. If you want all ingested documents to be used, remove `context_filter` altogether.
     *
     * When using `'include_sources': true`, the API will return the source Chunks used to create the response, which come from the context provided.
     *
     * When using `'stream': true`, the API will return data chunks following [OpenAI's streaming model](https://platform.openai.com/docs/api-reference/chat/streaming):
     * ```
     * {
         * "id":"12345",
         * "object":"completion.chunk",
         * "created":1694268190,
         * "model":"private-gpt",
         * "choices":[
             * {"index":0,"delta":{"content":"Hello"}, "finish_reason":null}
             * ]
             * }
             * ```
             *
             * Args:
             * request (Request): The HTTP request object.
             * body (CompletionsBody): The request body containing the completion prompt.
             *
             * Returns:
             * Union[OpenAICompletion, StreamingResponse]: The completion response.
             * @returns OpenAICompletion Successful Response
             * @throws ApiError
             */
            public static promptCompletionApiCompletionsPost({
                requestBody,
            }: {
                requestBody: CompletionsBody,
            }): CancelablePromise<OpenAICompletion> {
                return __request(OpenAPI, {
                    method: 'POST',
                    url: '/api/completions',
                    body: requestBody,
                    mediaType: 'application/json',
                    errors: {
                        422: `Validation Error`,
                    },
                });
            }

        }
