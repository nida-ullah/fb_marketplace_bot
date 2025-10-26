import Link from "next/link";
import { ArrowRight, Zap, Shield, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/Button";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Sticky Header (visible on scroll) */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60 border-b border-gray-200">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="text-2xl font-bold text-blue-600">
              FB Marketplace Bot
            </div>
            <div className="flex gap-3 sm:gap-4">
              <Link href="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link href="/signup">
                <Button>Get Started</Button>
              </Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Automate Your Facebook Marketplace
          <span className="block text-blue-600 mt-2">Posting at Scale</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Save hours of manual work. Post to multiple accounts, schedule
          listings, and manage everything from one powerful dashboard.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/signup">
            <Button size="lg" className="gap-2">
              Start Free Trial <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
          <Link href="/login">
            <Button size="lg" variant="outline">
              View Demo
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Why Choose Our Platform?
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {/* Card 1 */}
          <div className="text-center p-8 bg-white/90 backdrop-blur rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 text-blue-600 mb-4 ring-1 ring-blue-100">
              <Zap className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">
              Lightning Fast
            </h3>
            <p className="text-base leading-relaxed text-gray-700">
              Post to multiple accounts in seconds. Bulk upload hundreds of
              listings with just a CSV file.
            </p>
          </div>
          {/* Card 2 */}
          <div className="text-center p-8 bg-white/90 backdrop-blur rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-50 text-green-600 mb-4 ring-1 ring-green-100">
              <Shield className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">
              Secure & Reliable
            </h3>
            <p className="text-base leading-relaxed text-gray-700">
              Your accounts are safe with encrypted sessions. Login once and let
              the bot handle the rest.
            </p>
          </div>
          {/* Card 3 */}
          <div className="text-center p-8 bg-white/90 backdrop-blur rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-purple-50 text-purple-600 mb-4 ring-1 ring-purple-100">
              <TrendingUp className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">
              Scale Your Business
            </h3>
            <p className="text-base leading-relaxed text-gray-700">
              Manage unlimited accounts and posts. Track performance and
              optimize your marketplace strategy.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="bg-blue-600 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Automate Your Marketplace?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join hundreds of sellers who save time with automation
          </p>
          <Link href="/signup">
            <Button
              size="lg"
              variant="outline"
              className="bg-white text-blue-600 hover:bg-gray-100"
            >
              Get Started Now
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-600">
        <p>&copy; 2025 FB Marketplace Bot. All rights reserved.</p>
      </footer>
    </div>
  );
}
