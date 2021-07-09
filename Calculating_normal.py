import open3d as o3d
import numpy as np
import copy
import random

print("Testing mesh in open3d ...")
mesh = o3d.io.read_triangle_mesh("Desktop/open3d/processed_database/meshes/raw/apple/nontextured.ply")
print(mesh)
vertices = np.asarray(mesh.vertices)
contact1_index = random.randrange(vertices.shape[0])
contact2_index = random.randrange(vertices.shape[0])
print('Vertices:')
print(vertices)
contact1 = vertices[contact1_index]
contact2 = vertices[contact2_index]
print(contact1)
print(contact2)
contact_center = (contact2 + contact1)/2
print(f'Center of mesh: {mesh.get_center()}')
triangles = np.asarray(mesh.triangles)
print('Triangles:')
print(triangles)
print("")
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.01, origin=[0, 0, 0])
o3d.visualization.draw_geometries([mesh, mesh_frame])

def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = np.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens                
    return arr

#Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal
norm = np.zeros( vertices.shape, dtype=vertices.dtype )
#Create an indexed view into the vertex array using the array of three indices for triangles
tris = vertices[triangles]
#Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in each triangle             
n = np.cross( tris[::,1 ] - tris[::,0]  , tris[::,2 ] - tris[::,0] )
# n is now an array of normals per triangle. The length of each normal is dependent the vertices, 
# we need to normalize these, so that our next step weights each normal equally.
normalize_v3(n)
print('Normal vectors for triangles:')
print(normalize_v3(n))
print(normalize_v3(n).shape[0])
# now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
# But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle, 
# the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to normalize again afterwards.
# The cool part, we can actually add the normals through an indexed view of our (zeroed) per vertex normal array
norm[ triangles[:,0] ] += n
norm[ triangles[:,1] ] += n
norm[ triangles[:,2] ] += n
normalize_v3(norm)
print('Normal vectors for vertices:')
print(norm)
print(norm.shape[0])

# To render without the index list, we create a flattened array where
# the triangle indices are replaced with the actual vertices.

# first we create a single column index array
#tri_index = index_data.reshape( (-1) )        
# then we create an indexed view into our vertices and normals
va = vertices[ triangles ]
no = norm[ triangles ]        

# Then to render this in OpenGL
#from OpenGL import GL as gl
#def render():
#   gl.glEnableClientState( gl.GL_VERTEX_ARRAY )
#    gl.glEnableClientState( gl.GL_NORMAL_ARRAY )
#    gl.glVertexPointer( 3, gl.GL_FLOAT, 0, va )
#    gl.glNormalPointer( gl.GL_FLOAT,    0, no )
#    gl.glDrawArrays(gl.GL_TRIANGLES,    0, len(va) )



