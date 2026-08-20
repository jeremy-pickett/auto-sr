// navigator.clipboard.writeText silently rejects in a lot of ordinary
// situations -- an insecure context, a permissions policy that denies
// clipboard-write, an iframe without the right allow list -- and the
// old copy-link button swallowed that rejection, so all it visibly did
// was change the URL bar. This tries the modern API first and falls
// back to the old execCommand('copy') trick (a hidden, off-screen
// textarea, selected and copied synchronously) before giving up.
export async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    // fall through to the legacy path below
  }
  try {
    const area = document.createElement('textarea')
    area.value = text
    area.style.position = 'fixed'
    area.style.top = '-1000px'
    area.style.left = '-1000px'
    document.body.appendChild(area)
    area.focus()
    area.select()
    const ok = document.execCommand('copy')
    document.body.removeChild(area)
    return ok
  } catch {
    return false
  }
}
