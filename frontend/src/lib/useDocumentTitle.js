import { useEffect } from 'react'

// Sets the browser tab title while a view is mounted, restoring
// whatever it was before on unmount. Doesn't help link-preview
// crawlers (see index.html's Open Graph comment for why a hash-routed
// SPA can't do that server-side) -- this is purely for the human
// looking at their own tabs and bookmarks.
export function useDocumentTitle(title) {
  useEffect(() => {
    if (!title) return undefined
    const previous = document.title
    document.title = title
    return () => { document.title = previous }
  }, [title])
}
