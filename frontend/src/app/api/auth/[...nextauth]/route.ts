import NextAuth from "next-auth/next";
import axios from "axios";
import GoogleProvider from "next-auth/providers/google";

const handler = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    }),
  ],
  // secret: process.env.NEXTAUTH_SECRET,
  // callbacks: {
  //   async jwt({ token, user, account }): Promise<any> {
  //     if (user && account) {
  //       try {
  //         const response = await axios.post(
  //           `${process.env.NEXT_PUBLIC_API_URL}/auth/users/tokens`,
  //           {
  //             username: user.name,
  //             email: user.email,
  //             image: user.image,
  //             token: account.id_token
  //           },
  //           {
  //             headers: {
  //               "Content-Type": "application/json",
  //               "Secret-Key": process.env.NEXTAUTH_SECRET,
  //             },
  //           }
  //         );
  //         const data = await response.data;
  //         token.accessToken = data.access_token;
  //         token.refreshToken = data.refresh_token;
  //         // token.accessTokenExp = data.access_token_expires;
  //         token.userId = data.user.id;
  //       } catch (error) {
  //         console.error("Error access token", error)
  //         throw new Error("AccessTokenError");
  //       }
  //     }
  //     return Promise.resolve(token);
  //   },
  //   async session({ session, token }) {
  //     session.user = {
  //       name: session.user?.name,
  //       email: session.user?.email,
  //       image: session.user?.image,
  //       userId: token.userId,
  //     };
  //     session.access_token = token.accessToken;
  //     session.refresh_token = token.refreshToken;
  //     session.accessTokenExp = token.accessTokenExp;

  //     return session;
  //   },
  // },
});

export { handler as GET, handler as POST };
