/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Represents a message in the OpenAI conversation.
 *
 * Attributes:
 * content (str | None): The content of the message.
 * role (Literal["assistant", "system", "user"]): The role of the message sender. Defaults to "user".
 */
export type OpenAIMessage = {
    content: (string | null);
    role?: 'assistant' | 'system' | 'user';
};

