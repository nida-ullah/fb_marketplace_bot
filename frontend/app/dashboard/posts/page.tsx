"use client";

import { useEffect, useState } from "react";
import { postsAPI } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import {
  Package,
  CheckCircle,
  XCircle,
  Trash2,
  Plus,
  Edit,
  Calendar,
  DollarSign,
  Image as ImageIcon,
} from "lucide-react";
import Image from "next/image";

interface MarketplacePost {
  id: number;
  title: string;
  description: string;
  price: string;
  image: string;
  scheduled_time: string;
  posted: boolean;
  account: number;
  account_email: string;
}

export default function PostsPage() {
  const [posts, setPosts] = useState<MarketplacePost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState<"all" | "posted" | "pending">("all");

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await postsAPI.list();
      setPosts(response.data);
    } catch (err) {
      setError("Failed to load posts");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this post?")) return;

    try {
      await postsAPI.delete(id);
      setPosts(posts.filter((post) => post.id !== id));
    } catch (err) {
      alert("Failed to delete post");
      console.error(err);
    }
  };

  const filteredPosts = posts.filter((post) => {
    if (filter === "posted") return post.posted;
    if (filter === "pending") return !post.posted;
    return true;
  });

  const stats = {
    total: posts.length,
    posted: posts.filter((p) => p.posted).length,
    pending: posts.filter((p) => !p.posted).length,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading posts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Marketplace Posts
          </h1>
          <p className="mt-2 text-gray-600">
            Manage your Facebook Marketplace listings
          </p>
        </div>
        <Button variant="default" size="md">
          <Plus className="mr-2 h-5 w-5" />
          Create Post
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Posts</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
            <p className="text-xs text-muted-foreground">
              All marketplace listings
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Posted</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {stats.posted}
            </div>
            <p className="text-xs text-muted-foreground">Successfully posted</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending</CardTitle>
            <XCircle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {stats.pending}
            </div>
            <p className="text-xs text-muted-foreground">Awaiting posting</p>
          </CardContent>
        </Card>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2">
        <Button
          variant={filter === "all" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("all")}
        >
          All Posts ({stats.total})
        </Button>
        <Button
          variant={filter === "posted" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("posted")}
        >
          Posted ({stats.posted})
        </Button>
        <Button
          variant={filter === "pending" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("pending")}
        >
          Pending ({stats.pending})
        </Button>
      </div>

      {/* Posts Grid */}
      <Card>
        <CardHeader>
          <CardTitle>All Posts</CardTitle>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-md mb-4">
              {error}
            </div>
          )}

          {filteredPosts.length === 0 ? (
            <div className="text-center py-12">
              <Package className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                No posts found
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                {filter === "all"
                  ? "Get started by creating a new post."
                  : `No ${filter} posts available.`}
              </p>
              {filter === "all" && (
                <div className="mt-6">
                  <Button variant="default">
                    <Plus className="mr-2 h-5 w-5" />
                    Create Post
                  </Button>
                </div>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post) => (
                <div
                  key={post.id}
                  className="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
                >
                  {/* Post Image */}
                  <div className="relative h-48 bg-gray-200">
                    {post.image ? (
                      <Image
                        src={post.image}
                        alt={post.title}
                        fill
                        className="object-cover"
                      />
                    ) : (
                      <div className="flex items-center justify-center h-full">
                        <ImageIcon className="h-12 w-12 text-gray-400" />
                      </div>
                    )}
                  </div>

                  {/* Post Details */}
                  <div className="p-4 space-y-3">
                    {/* Title and Status */}
                    <div className="flex items-start justify-between gap-2">
                      <h3 className="font-semibold text-gray-900 line-clamp-2">
                        {post.title}
                      </h3>
                      {post.posted ? (
                        <span className="flex-shrink-0 px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                          <CheckCircle className="h-3 w-3 inline mr-1" />
                          Posted
                        </span>
                      ) : (
                        <span className="flex-shrink-0 px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                          <XCircle className="h-3 w-3 inline mr-1" />
                          Pending
                        </span>
                      )}
                    </div>

                    {/* Description */}
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {post.description}
                    </p>

                    {/* Price */}
                    <div className="flex items-center gap-2 text-lg font-bold text-blue-600">
                      <DollarSign className="h-5 w-5" />
                      {post.price}
                    </div>

                    {/* Account Email */}
                    <div className="text-xs text-gray-500 truncate">
                      Account: {post.account_email}
                    </div>

                    {/* Scheduled Time */}
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <Calendar className="h-4 w-4" />
                      {new Date(post.scheduled_time).toLocaleString()}
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 pt-2 border-t">
                      <Button
                        variant="outline"
                        size="sm"
                        className="flex-1"
                        onClick={() => alert("Edit functionality coming soon")}
                      >
                        <Edit size={16} className="mr-1" />
                        Edit
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        className="flex-1"
                        onClick={() => handleDelete(post.id)}
                      >
                        <Trash2 size={16} className="mr-1" />
                        Delete
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
