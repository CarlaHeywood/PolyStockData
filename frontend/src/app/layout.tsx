import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";
import { Input } from "@/components/ui/input";
import Link from "next/link";


const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InvestWise",
  description: "Finance app to analyze stocks and generate passive income",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const currentYear = new Date().getFullYear();

  return (
    <html lang="en" className="overflow-x-hidden h-100 m-0">
      <head>
        <link rel="icon" type="image/svg+xml" href="./favicon.svg" />
      </head>
      <body className={`${inter.className} overflow-x-hidden h-100 m-0`}>
        <div className="wrapper">
          <header className="w-full px-2 border-b-2">
            <div className="flex flex-cols items-center justify-between">
              {/* Logo */}
              <div className="flex items-center justify-start">
                <Link className="text-xl font-bold m-3" href="/">
                  InvestWise
                </Link>
              </div>
              <div className="flex items-center justify-end">
                <NavigationMenu className="w-screen">
                  <NavigationMenuList className="flex flex-cols items-center justify-between">
                    {/* Navigation */}
                    <div className="flex items-center justify-end space-x-2">
                      <NavigationMenuItem className="flex items-center">
                        <Link href="/dashboard" legacyBehavior passHref>
                          <NavigationMenuLink
                            className={navigationMenuTriggerStyle()}
                          >
                            Dashboard
                          </NavigationMenuLink>
                        </Link>
                      </NavigationMenuItem>
                      <NavigationMenuItem className="flex items-center">
                        {/* <form
                        onSubmit={handleSearchFormSubmit}
                        className="flex items-center"
                      >
                        <Input
                          // value={Input}
                          onChange={handleSearchInputChange}
                          placeholder="Search"
                        />
                      </form> */}
                        <Input placeholder="Search" />
                      </NavigationMenuItem>
                    </div>
                  </NavigationMenuList>
                </NavigationMenu>
              </div>
            </div>
          </header>
          <div>{children}</div>
          <footer className="footer text-center mx-3 my-5">
            <p>
              &copy; {currentYear} InvestWise. All rights reserved.
              <br />
              App by{" "}
              <Link href="https://carlaheywood.com" passHref>
                Carla
              </Link>
            </p>
          </footer>
        </div>
      </body>
    </html>
  );
}
