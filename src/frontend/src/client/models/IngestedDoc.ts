/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Represents an ingested document.
 *
 * Attributes:
 * object (Literal["ingest.document"]): The type of object.
 * doc_id (str): The ID of the document.
 * doc_metadata (dict[str, Any] | None): The metadata of the document.
 */
export type IngestedDoc = {
    object: any;
    doc_id: string;
    doc_metadata: (Record<string, any> | null);
};

