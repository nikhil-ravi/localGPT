/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { IngestedDoc } from './IngestedDoc';

/**
 * Represents the response returned by the ingest API.
 *
 * Attributes:
 * object (Literal["list"]): The type of object returned, which is always "list".
 * model (Literal["local-gpt"]): The name of the model used for ingestion, which is always "local-gpt".
 * data (list[IngestedDoc]): The list of ingested documents.
 */
export type IngestResponse = {
    object: any;
    model: any;
    data: Array<IngestedDoc>;
};

