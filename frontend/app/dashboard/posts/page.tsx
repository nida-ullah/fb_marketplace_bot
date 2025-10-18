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
  Grid,
  List,
} from "lucide-react";
import Image from "next/image";
import CreatePostModal from "@/components/CreatePostModal";
import { useToast, ToastContainer } from "@/components/ui/Toast";

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
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [viewMode, setViewMode] = useState<"grid" | "list">("list");
  const [selectedPosts, setSelectedPosts] = useState<number[]>([]);
  const [isDeleting, setIsDeleting] = useState(false);
  const { toasts, removeToast, success, error: showError } = useToast();

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
      setSelectedPosts(selectedPosts.filter((postId) => postId !== id));
      success("Post deleted successfully");
    } catch (err) {
      showError("Failed to delete post");
      console.error(err);
    }
  };

  const handleBulkDelete = async () => {
    if (selectedPosts.length === 0) {
      showError("Please select posts to delete");
      return;
    }

    if (
      !confirm(
        `Are you sure you want to delete ${selectedPosts.length} post(s)?`
      )
    )
      return;

    setIsDeleting(true);
    try {
      await Promise.all(selectedPosts.map((id) => postsAPI.delete(id)));
      setPosts(posts.filter((post) => !selectedPosts.includes(post.id)));
      success(`Successfully deleted ${selectedPosts.length} post(s)`);
      setSelectedPosts([]);
    } catch (err) {
      showError("Failed to delete some posts");
      console.error(err);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleSelectAll = () => {
    if (selectedPosts.length === filteredPosts.length) {
      setSelectedPosts([]);
    } else {
      setSelectedPosts(filteredPosts.map((post) => post.id));
    }
  };

  const handleSelectPost = (postId: number) => {
    if (selectedPosts.includes(postId)) {
      setSelectedPosts(selectedPosts.filter((id) => id !== postId));
    } else {
      setSelectedPosts([...selectedPosts, postId]);
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
      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} removeToast={removeToast} />

      {/* Create Post Modal */}
      <CreatePostModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSuccess={fetchPosts}
        onToast={(type, message) => {
          if (type === "success") success(message);
          else showError(message);
        }}
      />

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
        <Button
          variant="default"
          size="md"
          onClick={() => setIsCreateModalOpen(true)}
        >
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

      {/* Filter and View Controls */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
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

        <div className="flex gap-2">
          <Button
            variant={viewMode === "list" ? "default" : "outline"}
            size="sm"
            onClick={() => setViewMode("list")}
          >
            <List className="h-4 w-4 mr-2" />
            List
          </Button>
          <Button
            variant={viewMode === "grid" ? "default" : "outline"}
            size="sm"
            onClick={() => setViewMode("grid")}
          >
            <Grid className="h-4 w-4 mr-2" />
            Grid
          </Button>
        </div>
      </div>

      {/* Bulk Actions */}
      {selectedPosts.length > 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-blue-900">
                {selectedPosts.length} post(s) selected
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setSelectedPosts([])}
                >
                  Clear Selection
                </Button>
                {/* Start Posting Button - Only for pending posts */}
                {selectedPosts.some((id) => {
                  const post = posts.find((p) => p.id === id);
                  return post && !post.posted;
                }) && (
                  <Button
                    variant="default"
                    size="sm"
                    onClick={() => alert("Start Posting feature coming soon!")}
                    className="bg-green-600 hover:bg-green-700"
                  >
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Start Posting (
                    {
                      selectedPosts.filter((id) => {
                        const post = posts.find((p) => p.id === id);
                        return post && !post.posted;
                      }).length
                    }
                    )
                  </Button>
                )}
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={handleBulkDelete}
                  disabled={isDeleting}
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  {isDeleting
                    ? "Deleting..."
                    : `Delete ${selectedPosts.length}`}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Posts List/Grid */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>All Posts</CardTitle>
            {filteredPosts.length > 0 && (
              <Button variant="outline" size="sm" onClick={handleSelectAll}>
                {selectedPosts.length === filteredPosts.length
                  ? "Deselect All"
                  : "Select All"}
              </Button>
            )}
          </div>
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
                  <Button
                    variant="default"
                    onClick={() => setIsCreateModalOpen(true)}
                  >
                    <Plus className="mr-2 h-5 w-5" />
                    Create Post
                  </Button>
                </div>
              )}
            </div>
          ) : viewMode === "list" ? (
            // List View
            <div className="space-y-3">
              {filteredPosts.map((post) => (
                <div
                  key={post.id}
                  className={`border rounded-lg p-4 hover:bg-gray-50 transition-colors ${
                    selectedPosts.includes(post.id)
                      ? "bg-blue-50 border-blue-300"
                      : ""
                  }`}
                >
                  <div className="flex items-start gap-4">
                    {/* Checkbox */}
                    <input
                      type="checkbox"
                      checked={selectedPosts.includes(post.id)}
                      onChange={() => handleSelectPost(post.id)}
                      className="mt-1 h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500 cursor-pointer"
                      aria-label={`Select post: ${post.title}`}
                    />

                    {/* Image - Smaller thumbnail */}
                    <div className="relative w-20 h-20 flex-shrink-0 bg-gray-200 rounded-lg overflow-hidden">
                      {post.image ? (
                        <Image
                          src={post.image}
                          alt={post.title}
                          fill
                          className="object-cover"
                          sizes="80px"
                        />
                      ) : (
                        <div className="flex items-center justify-center h-full">
                          <ImageIcon className="h-8 w-8 text-gray-400" />
                        </div>
                      )}
                    </div>

                    {/* Post Details */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-gray-900 truncate">
                            {post.title}
                          </h3>
                          <p className="text-sm text-gray-600 line-clamp-2 mt-1">
                            {post.description}
                          </p>
                        </div>

                        {/* Status Badge */}
                        <div className="flex-shrink-0">
                          {post.posted ? (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              <CheckCircle className="h-3 w-3 mr-1" />
                              Posted
                            </span>
                          ) : (
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                              <XCircle className="h-3 w-3 mr-1" />
                              Pending
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Meta Information */}
                      <div className="flex items-center gap-4 mt-3 text-sm text-gray-500">
                        <div className="flex items-center gap-1 font-semibold text-blue-600">
                          <DollarSign className="h-4 w-4" />
                          {post.price}
                        </div>
                        <div className="flex items-center gap-1 truncate">
                          <span className="font-medium">Account:</span>
                          <span className="truncate">{post.account_email}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {new Date(post.scheduled_time).toLocaleDateString()}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex gap-2 mt-3">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() =>
                            alert("Edit functionality coming soon")
                          }
                        >
                          <Edit size={14} className="mr-1" />
                          Edit
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleDelete(post.id)}
                        >
                          <Trash2 size={14} className="mr-1" />
                          Delete
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            // Grid View (Original)
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredPosts.map((post) => (
                <div
                  key={post.id}
                  className={`border rounded-lg overflow-hidden hover:shadow-lg transition-all ${
                    selectedPosts.includes(post.id)
                      ? "ring-2 ring-blue-500"
                      : ""
                  }`}
                >
                  {/* Checkbox - Top Right Corner */}
                  <div className="relative">
                    <div className="absolute top-2 left-2 z-10">
                      <input
                        type="checkbox"
                        checked={selectedPosts.includes(post.id)}
                        onChange={() => handleSelectPost(post.id)}
                        className="h-5 w-5 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500 cursor-pointer bg-white shadow-sm"
                        aria-label={`Select post: ${post.title}`}
                      />
                    </div>

                    {/* Post Image - Smaller height */}
                    <div className="relative h-40 bg-gray-200">
                      {post.image ? (
                        <Image
                          src={post.image}
                          alt={post.title}
                          fill
                          className="object-cover"
                          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        />
                      ) : (
                        <div className="flex items-center justify-center h-full">
                          <ImageIcon className="h-12 w-12 text-gray-400" />
                        </div>
                      )}
                    </div>
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
