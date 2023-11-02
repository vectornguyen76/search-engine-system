"use client";
import React from "react";
import { signIn, signOut, useSession } from "next-auth/react";
const SigninButton = () => {
  const { data: session } = useSession();

  if (session && session.user) {
    return (
      <div className="flex gap-4 ml-auto">
        <p className="text-sky-600 px-3 py-1">{session.user.name}</p>
        <button
          onClick={() => signOut()}
          className="bg-orange-500 text-black-600 ml-auto px-3 py-1 border-solid rounded-full"
        >
          Sign Out
        </button>
      </div>
    );
  }
  return (
    <button
      onClick={() => signIn()}
      className="bg-green-500 text-black-600 ml-auto px-3 py-1 border-solid rounded-full"
    >
      Sign In
    </button>
  );
};

export default SigninButton;
