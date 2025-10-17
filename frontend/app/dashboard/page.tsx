"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Users, FileText, CheckCircle, Clock } from "lucide-react";
import { statsAPI } from "@/lib/api";
import { DashboardStats } from "@/types";

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await statsAPI.getDashboard();
      setStats(response.data);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
      // Set mock data for demo purposes
      setStats({
        total_accounts: 5,
        active_accounts: 4,
        total_posts: 120,
        pending_posts: 15,
        posted_today: 8,
        success_rate: 92.5,
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600 mx-auto"></div>
          <p className="mt-4 text-sm text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const statCards = [
    {
      title: "Total Accounts",
      value: stats?.total_accounts || 0,
      icon: Users,
      color: "text-blue-600",
      bgColor: "bg-blue-100",
    },
    {
      title: "Total Posts",
      value: stats?.total_posts || 0,
      icon: FileText,
      color: "text-green-600",
      bgColor: "bg-green-100",
    },
    {
      title: "Pending Posts",
      value: stats?.pending_posts || 0,
      icon: Clock,
      color: "text-yellow-600",
      bgColor: "bg-yellow-100",
    },
    {
      title: "Posted Today",
      value: stats?.posted_today || 0,
      icon: CheckCircle,
      color: "text-purple-600",
      bgColor: "bg-purple-100",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Welcome back! Here&apos;s an overview of your marketplace automation.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">
                {stat.title}
              </CardTitle>
              <div className={`rounded-full p-2 ${stat.bgColor}`}>
                <stat.icon className={`h-5 w-5 ${stat.color}`} />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Success Rate Card */}
      <Card>
        <CardHeader>
          <CardTitle>Success Rate</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
            <div className="text-4xl font-bold text-green-600">
              {stats?.success_rate || 0}%
            </div>
            <div className="flex-1">
              <div className="h-4 w-full rounded-full bg-gray-200">
                <div
                  className="h-4 rounded-full bg-green-600 transition-all"
                  style={{ width: `${stats?.success_rate || 0}%` }}
                />
              </div>
            </div>
          </div>
          <p className="mt-2 text-sm text-gray-600">
            Overall posting success rate across all accounts
          </p>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <a
              href="/dashboard/accounts"
              className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6 transition-colors hover:border-blue-600 hover:bg-blue-50"
            >
              <Users className="h-8 w-8 text-blue-600 mb-2" />
              <span className="font-medium">Manage Accounts</span>
            </a>
            <a
              href="/dashboard/posts"
              className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6 transition-colors hover:border-green-600 hover:bg-green-50"
            >
              <FileText className="h-8 w-8 text-green-600 mb-2" />
              <span className="font-medium">View Posts</span>
            </a>
            <a
              href="/dashboard/bulk-upload"
              className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 p-6 transition-colors hover:border-purple-600 hover:bg-purple-50"
            >
              <CheckCircle className="h-8 w-8 text-purple-600 mb-2" />
              <span className="font-medium">Bulk Upload</span>
            </a>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
