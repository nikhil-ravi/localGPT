import { ClearFiles } from "@/components/clear-files";
import { SidebarItems } from "@/components/sidebar/sidebar-items";
import { ThemeToggle } from "@/components/theme-toggle";

export type SidebarListProps = {
  files: string[];
  refreshFiles: () => Promise<void>;
};

export function SidebarList({ files, refreshFiles }: SidebarListProps) {
  return (
    <div className="flex flex-1 flex-col overflow-hidden">
      <div className="flex-1 overflow-auto">
        {files?.length ? (
          <div className="space-y-2 px-2">
            <SidebarItems files={files} refreshFiles={refreshFiles} />
          </div>
        ) : (
          <div className="p-8 text-center">
            <p className="text-sm text-muted-foreground">
              No files in the store
            </p>
          </div>
        )}
      </div>
      <div className="flex items-center justify-between p-4">
        <ThemeToggle />
        <ClearFiles isEnabled={files?.length > 0} refreshFiles={refreshFiles} />
      </div>
    </div>
  );
}
