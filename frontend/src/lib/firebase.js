import { useEffect, useState } from 'react'
import { initializeApp } from 'firebase/app'
import {
  getAuth,
  onAuthStateChanged,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
}

const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)

// One singleton auth instance; each component's useAuth() call sets
// up its own listener against it and they all update in lockstep — no
// Context needed for the handful of consumers this app has.
export function useAuth() {
  const [user, setUser] = useState(auth.currentUser)
  const [loading, setLoading] = useState(auth.currentUser === null)
  useEffect(() => onAuthStateChanged(auth, (u) => { setUser(u); setLoading(false) }), [])
  return { user, loading }
}

export const signInEmail = (email, password) => signInWithEmailAndPassword(auth, email, password)
export const signUpEmail = (email, password) => createUserWithEmailAndPassword(auth, email, password)
export const signOutUser = () => signOut(auth)

// The SDK handles caching/refresh internally, so this is safe to call
// on every request rather than bookkeeping a cached token ourselves.
export const getIdToken = () => (auth.currentUser ? auth.currentUser.getIdToken() : Promise.resolve(null))
