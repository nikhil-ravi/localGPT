import { IngestResponse } from "@/client"
import { fetcher } from "./utils"

export const dynamic = "force-dynamic";

export async function list_ingested_docs() {
    const ingested_docs = await fetcher(`${process.env.NEXT_PUBLIC_SITE_URL}/api/ingest/list`, {
        next: {
            revalidate: 0,
        },
    }) as IngestResponse
    return ingested_docs
}

export async function list_ingested_files() {
    const ingested_docs = await list_ingested_docs()
    // get the unique files from the ingested docs
    const fileNames: Set<string> = new Set()
    for (const doc of ingested_docs.data) {
        if (doc.doc_metadata === null) {
            continue
        }
        const fileName: string = doc.doc_metadata.file_name || "[FILE NAME MISSING]";
        fileNames.add(fileName)
    }
    return Array.from(fileNames)
}

export async function remove_all_files() {
    const ingested_docs = await list_ingested_docs()
    for (const doc of ingested_docs.data) {
        await fetch(`${process.env.NEXT_PUBLIC_SITE_URL}/api/ingest/${doc.doc_id}`, {
            method: 'DELETE',
        })
    }
    return
}

export async function remove_docs_for_file(file_name: string) {
    console.log("Removing docs for file: " + file_name)
    const ingested_docs = await list_ingested_docs()
    const docs_to_remove = ingested_docs.data.filter((doc) => {
        if (doc.doc_metadata === null) {
            return false
        }
        const fileName: string = doc.doc_metadata.file_name
        return fileName === file_name
    })
    console.log("Docs to delete: " + docs_to_remove)
    for (const doc of docs_to_remove) {
        await fetch(`${process.env.NEXT_PUBLIC_SITE_URL}/api/ingest/${doc.doc_id}`, {
            method: 'DELETE',
        })
    }
    return
}


export async function ingest_file(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await fetcher(`${process.env.NEXT_PUBLIC_SITE_URL}/api/ingest/file`, {
        method: 'POST',
        body: formData,
    }) as IngestResponse
    return response
}