/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_ingest_file_api_ingest_file_post } from '../models/Body_ingest_file_api_ingest_file_post';
import type { IngestResponse } from '../models/IngestResponse';
import type { IngestTextBody } from '../models/IngestTextBody';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class IngestService {

    /**
     * Ingest File
     * Ingests and processes a file, storing its chunks to be used as context.
     *
     * The context obtained from files is later used in `/chat/completions`, `/completions`, and `/chunks` APIs.
     *
     * Most common document formats are supported, but you may be prompted to install an extra dependency to manage a specific file type.
     *
     * A file can generate different Documents (for example a PDF generates one Document per page). All Documents IDs are returned in the response, together with the extracted Metadata (which is later used to improve context retrieval). Those IDs can be used to filter the context used to create responses in `/chat/completions`, `/completions`, and `/chunks` APIs.
     *
     * Args:
     * request (Request): The incoming request object.
     * file (UploadFile): The file to be ingested.
     *
     * Returns:
     * IngestResponse: The response containing the ingested documents.
     * @returns IngestResponse Successful Response
     * @throws ApiError
     */
    public static ingestFileApiIngestFilePost({
        formData,
    }: {
        formData: Body_ingest_file_api_ingest_file_post,
    }): CancelablePromise<IngestResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/ingest/file',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Ingest Text
     * Ingests and processes a text, storing its chunks to be used as context.
     *
     * The context obtained from files is later used in `/chat/completions`, `/completions`, and `/chunks` APIs.
     *
     * A Document will be generated with the given text. The Document ID is returned in the response, together with the extracted Metadata (which is later used to improve context retrieval). That ID can be used to filter the context used to create responses in `/chat/completions`, `/completions`, and `/chunks` APIs.
     *
     * Args:
     * request (Request): The incoming request object.
     * body (IngestTextBody): The request body containing the file name and text.
     *
     * Returns:
     * IngestResponse: The response object containing the ingested documents.
     * @returns IngestResponse Successful Response
     * @throws ApiError
     */
    public static ingestTextApiIngestTextPost({
        requestBody,
    }: {
        requestBody: IngestTextBody,
    }): CancelablePromise<IngestResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/ingest/text',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Ingested
     * "Lists already ingested Documents including their Document ID and metadata.
     *
     * Those IDs can be used to filter the context used to create responses
     * in `/chat/completions`, `/completions`, and `/chunks` APIs.
     *
     * Args:
     * request (Request): The request object.
     *
     * Returns:
     * IngestResponse: The response object containing the list of ingested documents.
     * @returns IngestResponse Successful Response
     * @throws ApiError
     */
    public static listIngestedApiIngestListGet(): CancelablePromise<IngestResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/ingest/list',
        });
    }

    /**
     * Delete Ingested
     * "Delete the specified ingested Document.
     *
     * The `doc_id` can be obtained from the `GET /ingest/list` endpoint. The document will be effectively deleted from your storage context.
     *
     * Args:
     * request (Request): The request object.
     * doc_id (str): The ID of the document to be deleted.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteIngestedApiIngestDocIdDelete({
        docId,
    }: {
        docId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/ingest/{doc_id}',
            path: {
                'doc_id': docId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
