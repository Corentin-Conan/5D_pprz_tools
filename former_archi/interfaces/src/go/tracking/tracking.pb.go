// Code generated by protoc-gen-go. DO NOT EDIT.
// source: tracking/tracking.proto

package tracking

import (
	context "context"
	fmt "fmt"
	_ "github.com/airmap/interfaces/src/go"
	system "github.com/airmap/interfaces/src/go/system"
	proto "github.com/golang/protobuf/proto"
	duration "github.com/golang/protobuf/ptypes/duration"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

// ConnectProviderParameters models configuration parameters for provider streams.
type ConnectProviderParameters struct {
	// The ID of the provider.
	Id *Identity_ProviderId `protobuf:"bytes,1,opt,name=id,proto3" json:"id,omitempty"`
	// The expected duration between updates. Used for monitoring and alerting
	// purposes. If null, the pipeline chooses a default value or tries to
	// determine a reasonable value based on historic data.
	ExpectedDurationBetweenUpdates *duration.Duration `protobuf:"bytes,2,opt,name=expected_duration_between_updates,json=expectedDurationBetweenUpdates,proto3" json:"expected_duration_between_updates,omitempty"`
	XXX_NoUnkeyedLiteral           struct{}           `json:"-"`
	XXX_unrecognized               []byte             `json:"-"`
	XXX_sizecache                  int32              `json:"-"`
}

func (m *ConnectProviderParameters) Reset()         { *m = ConnectProviderParameters{} }
func (m *ConnectProviderParameters) String() string { return proto.CompactTextString(m) }
func (*ConnectProviderParameters) ProtoMessage()    {}
func (*ConnectProviderParameters) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{0}
}

func (m *ConnectProviderParameters) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ConnectProviderParameters.Unmarshal(m, b)
}
func (m *ConnectProviderParameters) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ConnectProviderParameters.Marshal(b, m, deterministic)
}
func (m *ConnectProviderParameters) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ConnectProviderParameters.Merge(m, src)
}
func (m *ConnectProviderParameters) XXX_Size() int {
	return xxx_messageInfo_ConnectProviderParameters.Size(m)
}
func (m *ConnectProviderParameters) XXX_DiscardUnknown() {
	xxx_messageInfo_ConnectProviderParameters.DiscardUnknown(m)
}

var xxx_messageInfo_ConnectProviderParameters proto.InternalMessageInfo

func (m *ConnectProviderParameters) GetId() *Identity_ProviderId {
	if m != nil {
		return m.Id
	}
	return nil
}

func (m *ConnectProviderParameters) GetExpectedDurationBetweenUpdates() *duration.Duration {
	if m != nil {
		return m.ExpectedDurationBetweenUpdates
	}
	return nil
}

// ConnectProcessorParameters models configuration parameters for processor streams
type ConnectProcessorParameters struct {
	EnableProjection     bool     `protobuf:"varint,1,opt,name=enable_projection,json=enableProjection,proto3" json:"enable_projection,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *ConnectProcessorParameters) Reset()         { *m = ConnectProcessorParameters{} }
func (m *ConnectProcessorParameters) String() string { return proto.CompactTextString(m) }
func (*ConnectProcessorParameters) ProtoMessage()    {}
func (*ConnectProcessorParameters) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{1}
}

func (m *ConnectProcessorParameters) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ConnectProcessorParameters.Unmarshal(m, b)
}
func (m *ConnectProcessorParameters) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ConnectProcessorParameters.Marshal(b, m, deterministic)
}
func (m *ConnectProcessorParameters) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ConnectProcessorParameters.Merge(m, src)
}
func (m *ConnectProcessorParameters) XXX_Size() int {
	return xxx_messageInfo_ConnectProcessorParameters.Size(m)
}
func (m *ConnectProcessorParameters) XXX_DiscardUnknown() {
	xxx_messageInfo_ConnectProcessorParameters.DiscardUnknown(m)
}

var xxx_messageInfo_ConnectProcessorParameters proto.InternalMessageInfo

func (m *ConnectProcessorParameters) GetEnableProjection() bool {
	if m != nil {
		return m.EnableProjection
	}
	return false
}

// Update bundles types used in the exchange of tracks.
type Update struct {
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Update) Reset()         { *m = Update{} }
func (m *Update) String() string { return proto.CompactTextString(m) }
func (*Update) ProtoMessage()    {}
func (*Update) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{2}
}

func (m *Update) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Update.Unmarshal(m, b)
}
func (m *Update) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Update.Marshal(b, m, deterministic)
}
func (m *Update) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Update.Merge(m, src)
}
func (m *Update) XXX_Size() int {
	return xxx_messageInfo_Update.Size(m)
}
func (m *Update) XXX_DiscardUnknown() {
	xxx_messageInfo_Update.DiscardUnknown(m)
}

var xxx_messageInfo_Update proto.InternalMessageInfo

// FromProvider wraps messages being sent by a provider to a traffic collector.
type Update_FromProvider struct {
	// Types that are valid to be assigned to Details:
	//	*Update_FromProvider_Status
	//	*Update_FromProvider_Batch
	//	*Update_FromProvider_Params
	Details              isUpdate_FromProvider_Details `protobuf_oneof:"details"`
	XXX_NoUnkeyedLiteral struct{}                      `json:"-"`
	XXX_unrecognized     []byte                        `json:"-"`
	XXX_sizecache        int32                         `json:"-"`
}

func (m *Update_FromProvider) Reset()         { *m = Update_FromProvider{} }
func (m *Update_FromProvider) String() string { return proto.CompactTextString(m) }
func (*Update_FromProvider) ProtoMessage()    {}
func (*Update_FromProvider) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{2, 0}
}

func (m *Update_FromProvider) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Update_FromProvider.Unmarshal(m, b)
}
func (m *Update_FromProvider) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Update_FromProvider.Marshal(b, m, deterministic)
}
func (m *Update_FromProvider) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Update_FromProvider.Merge(m, src)
}
func (m *Update_FromProvider) XXX_Size() int {
	return xxx_messageInfo_Update_FromProvider.Size(m)
}
func (m *Update_FromProvider) XXX_DiscardUnknown() {
	xxx_messageInfo_Update_FromProvider.DiscardUnknown(m)
}

var xxx_messageInfo_Update_FromProvider proto.InternalMessageInfo

type isUpdate_FromProvider_Details interface {
	isUpdate_FromProvider_Details()
}

type Update_FromProvider_Status struct {
	Status *system.Status `protobuf:"bytes,1,opt,name=status,proto3,oneof"`
}

type Update_FromProvider_Batch struct {
	Batch *Track_Batch `protobuf:"bytes,2,opt,name=batch,proto3,oneof"`
}

type Update_FromProvider_Params struct {
	Params *ConnectProviderParameters `protobuf:"bytes,3,opt,name=params,proto3,oneof"`
}

func (*Update_FromProvider_Status) isUpdate_FromProvider_Details() {}

func (*Update_FromProvider_Batch) isUpdate_FromProvider_Details() {}

func (*Update_FromProvider_Params) isUpdate_FromProvider_Details() {}

func (m *Update_FromProvider) GetDetails() isUpdate_FromProvider_Details {
	if m != nil {
		return m.Details
	}
	return nil
}

func (m *Update_FromProvider) GetStatus() *system.Status {
	if x, ok := m.GetDetails().(*Update_FromProvider_Status); ok {
		return x.Status
	}
	return nil
}

func (m *Update_FromProvider) GetBatch() *Track_Batch {
	if x, ok := m.GetDetails().(*Update_FromProvider_Batch); ok {
		return x.Batch
	}
	return nil
}

func (m *Update_FromProvider) GetParams() *ConnectProviderParameters {
	if x, ok := m.GetDetails().(*Update_FromProvider_Params); ok {
		return x.Params
	}
	return nil
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*Update_FromProvider) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*Update_FromProvider_Status)(nil),
		(*Update_FromProvider_Batch)(nil),
		(*Update_FromProvider_Params)(nil),
	}
}

// ToProvider wraps messages being sent from a collector back to a provider.
type Update_ToProvider struct {
	// Types that are valid to be assigned to Details:
	//	*Update_ToProvider_Status
	//	*Update_ToProvider_Ack
	//	*Update_ToProvider_Nack
	Details              isUpdate_ToProvider_Details `protobuf_oneof:"details"`
	XXX_NoUnkeyedLiteral struct{}                    `json:"-"`
	XXX_unrecognized     []byte                      `json:"-"`
	XXX_sizecache        int32                       `json:"-"`
}

func (m *Update_ToProvider) Reset()         { *m = Update_ToProvider{} }
func (m *Update_ToProvider) String() string { return proto.CompactTextString(m) }
func (*Update_ToProvider) ProtoMessage()    {}
func (*Update_ToProvider) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{2, 1}
}

func (m *Update_ToProvider) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Update_ToProvider.Unmarshal(m, b)
}
func (m *Update_ToProvider) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Update_ToProvider.Marshal(b, m, deterministic)
}
func (m *Update_ToProvider) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Update_ToProvider.Merge(m, src)
}
func (m *Update_ToProvider) XXX_Size() int {
	return xxx_messageInfo_Update_ToProvider.Size(m)
}
func (m *Update_ToProvider) XXX_DiscardUnknown() {
	xxx_messageInfo_Update_ToProvider.DiscardUnknown(m)
}

var xxx_messageInfo_Update_ToProvider proto.InternalMessageInfo

type isUpdate_ToProvider_Details interface {
	isUpdate_ToProvider_Details()
}

type Update_ToProvider_Status struct {
	Status *system.Status `protobuf:"bytes,1,opt,name=status,proto3,oneof"`
}

type Update_ToProvider_Ack struct {
	Ack *system.Ack `protobuf:"bytes,2,opt,name=ack,proto3,oneof"`
}

type Update_ToProvider_Nack struct {
	Nack *system.Nack `protobuf:"bytes,3,opt,name=nack,proto3,oneof"`
}

func (*Update_ToProvider_Status) isUpdate_ToProvider_Details() {}

func (*Update_ToProvider_Ack) isUpdate_ToProvider_Details() {}

func (*Update_ToProvider_Nack) isUpdate_ToProvider_Details() {}

func (m *Update_ToProvider) GetDetails() isUpdate_ToProvider_Details {
	if m != nil {
		return m.Details
	}
	return nil
}

func (m *Update_ToProvider) GetStatus() *system.Status {
	if x, ok := m.GetDetails().(*Update_ToProvider_Status); ok {
		return x.Status
	}
	return nil
}

func (m *Update_ToProvider) GetAck() *system.Ack {
	if x, ok := m.GetDetails().(*Update_ToProvider_Ack); ok {
		return x.Ack
	}
	return nil
}

func (m *Update_ToProvider) GetNack() *system.Nack {
	if x, ok := m.GetDetails().(*Update_ToProvider_Nack); ok {
		return x.Nack
	}
	return nil
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*Update_ToProvider) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*Update_ToProvider_Status)(nil),
		(*Update_ToProvider_Ack)(nil),
		(*Update_ToProvider_Nack)(nil),
	}
}

// ToProcessor wraps messages being sent by a collector to a processor.
type Update_ToProcessor struct {
	// Types that are valid to be assigned to Details:
	//	*Update_ToProcessor_Status
	//	*Update_ToProcessor_Batch
	Details              isUpdate_ToProcessor_Details `protobuf_oneof:"details"`
	XXX_NoUnkeyedLiteral struct{}                     `json:"-"`
	XXX_unrecognized     []byte                       `json:"-"`
	XXX_sizecache        int32                        `json:"-"`
}

func (m *Update_ToProcessor) Reset()         { *m = Update_ToProcessor{} }
func (m *Update_ToProcessor) String() string { return proto.CompactTextString(m) }
func (*Update_ToProcessor) ProtoMessage()    {}
func (*Update_ToProcessor) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{2, 2}
}

func (m *Update_ToProcessor) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Update_ToProcessor.Unmarshal(m, b)
}
func (m *Update_ToProcessor) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Update_ToProcessor.Marshal(b, m, deterministic)
}
func (m *Update_ToProcessor) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Update_ToProcessor.Merge(m, src)
}
func (m *Update_ToProcessor) XXX_Size() int {
	return xxx_messageInfo_Update_ToProcessor.Size(m)
}
func (m *Update_ToProcessor) XXX_DiscardUnknown() {
	xxx_messageInfo_Update_ToProcessor.DiscardUnknown(m)
}

var xxx_messageInfo_Update_ToProcessor proto.InternalMessageInfo

type isUpdate_ToProcessor_Details interface {
	isUpdate_ToProcessor_Details()
}

type Update_ToProcessor_Status struct {
	Status *system.Status `protobuf:"bytes,1,opt,name=status,proto3,oneof"`
}

type Update_ToProcessor_Batch struct {
	Batch *Track_Batch `protobuf:"bytes,2,opt,name=batch,proto3,oneof"`
}

func (*Update_ToProcessor_Status) isUpdate_ToProcessor_Details() {}

func (*Update_ToProcessor_Batch) isUpdate_ToProcessor_Details() {}

func (m *Update_ToProcessor) GetDetails() isUpdate_ToProcessor_Details {
	if m != nil {
		return m.Details
	}
	return nil
}

func (m *Update_ToProcessor) GetStatus() *system.Status {
	if x, ok := m.GetDetails().(*Update_ToProcessor_Status); ok {
		return x.Status
	}
	return nil
}

func (m *Update_ToProcessor) GetBatch() *Track_Batch {
	if x, ok := m.GetDetails().(*Update_ToProcessor_Batch); ok {
		return x.Batch
	}
	return nil
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*Update_ToProcessor) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*Update_ToProcessor_Status)(nil),
		(*Update_ToProcessor_Batch)(nil),
	}
}

type Update_FromProcessor struct {
	// Types that are valid to be assigned to Details:
	//	*Update_FromProcessor_Status
	//	*Update_FromProcessor_Ack
	//	*Update_FromProcessor_Params
	Details              isUpdate_FromProcessor_Details `protobuf_oneof:"details"`
	XXX_NoUnkeyedLiteral struct{}                       `json:"-"`
	XXX_unrecognized     []byte                         `json:"-"`
	XXX_sizecache        int32                          `json:"-"`
}

func (m *Update_FromProcessor) Reset()         { *m = Update_FromProcessor{} }
func (m *Update_FromProcessor) String() string { return proto.CompactTextString(m) }
func (*Update_FromProcessor) ProtoMessage()    {}
func (*Update_FromProcessor) Descriptor() ([]byte, []int) {
	return fileDescriptor_ef03cdca4d8d01dd, []int{2, 3}
}

func (m *Update_FromProcessor) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Update_FromProcessor.Unmarshal(m, b)
}
func (m *Update_FromProcessor) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Update_FromProcessor.Marshal(b, m, deterministic)
}
func (m *Update_FromProcessor) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Update_FromProcessor.Merge(m, src)
}
func (m *Update_FromProcessor) XXX_Size() int {
	return xxx_messageInfo_Update_FromProcessor.Size(m)
}
func (m *Update_FromProcessor) XXX_DiscardUnknown() {
	xxx_messageInfo_Update_FromProcessor.DiscardUnknown(m)
}

var xxx_messageInfo_Update_FromProcessor proto.InternalMessageInfo

type isUpdate_FromProcessor_Details interface {
	isUpdate_FromProcessor_Details()
}

type Update_FromProcessor_Status struct {
	Status *system.Status `protobuf:"bytes,1,opt,name=status,proto3,oneof"`
}

type Update_FromProcessor_Ack struct {
	Ack *system.Ack `protobuf:"bytes,2,opt,name=ack,proto3,oneof"`
}

type Update_FromProcessor_Params struct {
	Params *ConnectProcessorParameters `protobuf:"bytes,3,opt,name=params,proto3,oneof"`
}

func (*Update_FromProcessor_Status) isUpdate_FromProcessor_Details() {}

func (*Update_FromProcessor_Ack) isUpdate_FromProcessor_Details() {}

func (*Update_FromProcessor_Params) isUpdate_FromProcessor_Details() {}

func (m *Update_FromProcessor) GetDetails() isUpdate_FromProcessor_Details {
	if m != nil {
		return m.Details
	}
	return nil
}

func (m *Update_FromProcessor) GetStatus() *system.Status {
	if x, ok := m.GetDetails().(*Update_FromProcessor_Status); ok {
		return x.Status
	}
	return nil
}

func (m *Update_FromProcessor) GetAck() *system.Ack {
	if x, ok := m.GetDetails().(*Update_FromProcessor_Ack); ok {
		return x.Ack
	}
	return nil
}

func (m *Update_FromProcessor) GetParams() *ConnectProcessorParameters {
	if x, ok := m.GetDetails().(*Update_FromProcessor_Params); ok {
		return x.Params
	}
	return nil
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*Update_FromProcessor) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*Update_FromProcessor_Status)(nil),
		(*Update_FromProcessor_Ack)(nil),
		(*Update_FromProcessor_Params)(nil),
	}
}

func init() {
	proto.RegisterType((*ConnectProviderParameters)(nil), "tracking.ConnectProviderParameters")
	proto.RegisterType((*ConnectProcessorParameters)(nil), "tracking.ConnectProcessorParameters")
	proto.RegisterType((*Update)(nil), "tracking.Update")
	proto.RegisterType((*Update_FromProvider)(nil), "tracking.Update.FromProvider")
	proto.RegisterType((*Update_ToProvider)(nil), "tracking.Update.ToProvider")
	proto.RegisterType((*Update_ToProcessor)(nil), "tracking.Update.ToProcessor")
	proto.RegisterType((*Update_FromProcessor)(nil), "tracking.Update.FromProcessor")
}

func init() { proto.RegisterFile("tracking/tracking.proto", fileDescriptor_ef03cdca4d8d01dd) }

var fileDescriptor_ef03cdca4d8d01dd = []byte{
	// 544 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xb4, 0x54, 0x41, 0x6f, 0x12, 0x41,
	0x14, 0x66, 0x29, 0x62, 0xfb, 0xa8, 0x8a, 0xa3, 0x46, 0xba, 0x5a, 0x54, 0xf4, 0x40, 0xa2, 0xdd,
	0x35, 0xf5, 0xac, 0x89, 0xd4, 0x18, 0xb8, 0x18, 0x5c, 0xf1, 0xe2, 0x85, 0xcc, 0xce, 0xbe, 0xd2,
	0x29, 0x30, 0xb3, 0xce, 0x0c, 0xda, 0xde, 0x3c, 0xf9, 0x4f, 0xf4, 0x6e, 0x62, 0xfc, 0x3d, 0xfe,
	0x14, 0xb3, 0x3b, 0x3b, 0x80, 0x48, 0x63, 0x34, 0xe9, 0x0d, 0xbe, 0xef, 0xcd, 0xf7, 0xbe, 0xf7,
	0xbe, 0x99, 0x85, 0x9b, 0x46, 0x51, 0x36, 0xe6, 0x62, 0x14, 0xba, 0x1f, 0x41, 0xaa, 0xa4, 0x91,
	0x64, 0xd3, 0xfd, 0xf7, 0x9b, 0x23, 0x29, 0x47, 0x13, 0x0c, 0x73, 0x3c, 0x9e, 0x1d, 0x86, 0xc9,
	0x4c, 0x51, 0xc3, 0xa5, 0xb0, 0x95, 0x7e, 0x1d, 0x4f, 0x0c, 0x0a, 0xcd, 0xa5, 0xd0, 0x05, 0x72,
	0x4d, 0x9f, 0x6a, 0x83, 0xd3, 0x50, 0x1b, 0x6a, 0x66, 0x0e, 0xac, 0x17, 0x20, 0x65, 0xe3, 0x02,
	0x59, 0xf4, 0xe6, 0x09, 0x0a, 0xc3, 0xcd, 0x69, 0x41, 0x5c, 0xff, 0xdd, 0x94, 0x45, 0x5b, 0x3f,
	0x3c, 0xd8, 0x39, 0x90, 0x42, 0x20, 0x33, 0x7d, 0x25, 0x3f, 0xf0, 0x04, 0x55, 0x9f, 0x2a, 0x3a,
	0x45, 0x83, 0x4a, 0x93, 0x3d, 0x28, 0xf3, 0xa4, 0xe1, 0xdd, 0xf5, 0xda, 0xb5, 0xfd, 0xdd, 0x60,
	0x3e, 0x4c, 0xcf, 0x29, 0xbb, 0x23, 0xbd, 0x24, 0x2a, 0xf3, 0x84, 0x1c, 0xc3, 0x3d, 0x3c, 0x49,
	0x91, 0x19, 0x4c, 0x86, 0x6e, 0x9e, 0x61, 0x8c, 0xe6, 0x23, 0xa2, 0x18, 0xce, 0xd2, 0x84, 0x1a,
	0xd4, 0x8d, 0x72, 0xae, 0xb6, 0x13, 0xd8, 0x05, 0x04, 0x6e, 0x01, 0xc1, 0x8b, 0xe2, 0x40, 0xa7,
	0xf2, 0xe9, 0xeb, 0xae, 0x17, 0x35, 0x9d, 0xd2, 0x1c, 0xb7, 0x3a, 0x6f, 0xad, 0x4c, 0xab, 0x07,
	0xfe, 0xc2, 0x37, 0x43, 0xad, 0xe5, 0xb2, 0xf1, 0x87, 0x70, 0x15, 0x05, 0x8d, 0x27, 0x38, 0x4c,
	0x95, 0x3c, 0x46, 0x96, 0x09, 0xe4, 0x73, 0x6c, 0x46, 0x75, 0x4b, 0xf4, 0xe7, 0x78, 0xeb, 0x67,
	0x05, 0xaa, 0x56, 0xd6, 0xff, 0xe6, 0xc1, 0xf6, 0x4b, 0x25, 0xa7, 0x6e, 0x30, 0xd2, 0x86, 0xaa,
	0x5d, 0x78, 0xb1, 0x85, 0xcb, 0x81, 0xdd, 0x78, 0xf0, 0x26, 0x47, 0xbb, 0xa5, 0xa8, 0xe0, 0xc9,
	0x1e, 0x5c, 0x88, 0xa9, 0x61, 0x47, 0xc5, 0x80, 0x37, 0x16, 0xeb, 0x1a, 0xe4, 0xfb, 0xee, 0x64,
	0x64, 0xb7, 0x14, 0xd9, 0x2a, 0xf2, 0x14, 0xaa, 0x69, 0xe6, 0x57, 0x37, 0x36, 0xf2, 0xfa, 0xfb,
	0x8b, 0xfa, 0x33, 0xf3, 0xc8, 0xba, 0xd9, 0x43, 0x9d, 0x2d, 0xb8, 0x98, 0xa0, 0xa1, 0x7c, 0xa2,
	0xfd, 0xcf, 0x1e, 0xc0, 0x40, 0xfe, 0x87, 0xe3, 0x3b, 0xb0, 0x41, 0xd9, 0xb8, 0xf0, 0x5b, 0x73,
	0x65, 0xcf, 0xd9, 0xb8, 0x5b, 0x8a, 0x32, 0x86, 0xb4, 0xa0, 0x22, 0xb2, 0x0a, 0xeb, 0x70, 0xdb,
	0x55, 0xbc, 0xa2, 0x79, 0x49, 0xce, 0x2d, 0x1b, 0x79, 0x0f, 0xb5, 0xdc, 0x87, 0x4d, 0xe3, 0xdc,
	0x56, 0xb7, 0xdc, 0xf2, 0x8b, 0x07, 0x97, 0x8a, 0xbc, 0xfe, 0xb9, 0xeb, 0x5f, 0xc7, 0x7f, 0xb6,
	0x12, 0xd1, 0x83, 0x75, 0x11, 0xad, 0x5e, 0xbd, 0xb5, 0x19, 0xed, 0x7f, 0xf7, 0x60, 0xeb, 0x40,
	0x4e, 0x26, 0xc8, 0x8c, 0x54, 0xe4, 0x35, 0x5c, 0x59, 0xc9, 0x98, 0x2c, 0xbd, 0x2e, 0x7b, 0x15,
	0x83, 0xe5, 0x6b, 0xe8, 0xdf, 0xfa, 0x83, 0x5e, 0x24, 0xde, 0xf6, 0x1e, 0x7b, 0x64, 0x00, 0xf5,
	0x55, 0x4f, 0xa4, 0x79, 0x96, 0xa6, 0xe5, 0xfd, 0xdb, 0xeb, 0x45, 0x2d, 0x9b, 0xa9, 0x76, 0x82,
	0x77, 0x8f, 0x46, 0xdc, 0x1c, 0xcd, 0xe2, 0x80, 0xc9, 0x69, 0x48, 0xb9, 0x9a, 0xd2, 0x34, 0xe4,
	0xc2, 0xa0, 0x3a, 0xa4, 0x0c, 0x75, 0xa8, 0x15, 0x0b, 0x47, 0x72, 0xfe, 0x95, 0x8b, 0xab, 0xf9,
	0x6b, 0x7e, 0xf2, 0x2b, 0x00, 0x00, 0xff, 0xff, 0xb3, 0x09, 0xbd, 0x9c, 0x01, 0x05, 0x00, 0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// CollectorClient is the client API for Collector service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type CollectorClient interface {
	// ConnectProvider connects a stream of updates from a provider to a collector.
	ConnectProvider(ctx context.Context, opts ...grpc.CallOption) (Collector_ConnectProviderClient, error)
	// ConnectProcessor connects a stream of updates from a collector to a processor.
	ConnectProcessor(ctx context.Context, opts ...grpc.CallOption) (Collector_ConnectProcessorClient, error)
}

type collectorClient struct {
	cc *grpc.ClientConn
}

func NewCollectorClient(cc *grpc.ClientConn) CollectorClient {
	return &collectorClient{cc}
}

func (c *collectorClient) ConnectProvider(ctx context.Context, opts ...grpc.CallOption) (Collector_ConnectProviderClient, error) {
	stream, err := c.cc.NewStream(ctx, &_Collector_serviceDesc.Streams[0], "/tracking.Collector/ConnectProvider", opts...)
	if err != nil {
		return nil, err
	}
	x := &collectorConnectProviderClient{stream}
	return x, nil
}

type Collector_ConnectProviderClient interface {
	Send(*Update_FromProvider) error
	Recv() (*Update_ToProvider, error)
	grpc.ClientStream
}

type collectorConnectProviderClient struct {
	grpc.ClientStream
}

func (x *collectorConnectProviderClient) Send(m *Update_FromProvider) error {
	return x.ClientStream.SendMsg(m)
}

func (x *collectorConnectProviderClient) Recv() (*Update_ToProvider, error) {
	m := new(Update_ToProvider)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *collectorClient) ConnectProcessor(ctx context.Context, opts ...grpc.CallOption) (Collector_ConnectProcessorClient, error) {
	stream, err := c.cc.NewStream(ctx, &_Collector_serviceDesc.Streams[1], "/tracking.Collector/ConnectProcessor", opts...)
	if err != nil {
		return nil, err
	}
	x := &collectorConnectProcessorClient{stream}
	return x, nil
}

type Collector_ConnectProcessorClient interface {
	Send(*Update_FromProcessor) error
	Recv() (*Update_ToProcessor, error)
	grpc.ClientStream
}

type collectorConnectProcessorClient struct {
	grpc.ClientStream
}

func (x *collectorConnectProcessorClient) Send(m *Update_FromProcessor) error {
	return x.ClientStream.SendMsg(m)
}

func (x *collectorConnectProcessorClient) Recv() (*Update_ToProcessor, error) {
	m := new(Update_ToProcessor)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// CollectorServer is the server API for Collector service.
type CollectorServer interface {
	// ConnectProvider connects a stream of updates from a provider to a collector.
	ConnectProvider(Collector_ConnectProviderServer) error
	// ConnectProcessor connects a stream of updates from a collector to a processor.
	ConnectProcessor(Collector_ConnectProcessorServer) error
}

// UnimplementedCollectorServer can be embedded to have forward compatible implementations.
type UnimplementedCollectorServer struct {
}

func (*UnimplementedCollectorServer) ConnectProvider(srv Collector_ConnectProviderServer) error {
	return status.Errorf(codes.Unimplemented, "method ConnectProvider not implemented")
}
func (*UnimplementedCollectorServer) ConnectProcessor(srv Collector_ConnectProcessorServer) error {
	return status.Errorf(codes.Unimplemented, "method ConnectProcessor not implemented")
}

func RegisterCollectorServer(s *grpc.Server, srv CollectorServer) {
	s.RegisterService(&_Collector_serviceDesc, srv)
}

func _Collector_ConnectProvider_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(CollectorServer).ConnectProvider(&collectorConnectProviderServer{stream})
}

type Collector_ConnectProviderServer interface {
	Send(*Update_ToProvider) error
	Recv() (*Update_FromProvider, error)
	grpc.ServerStream
}

type collectorConnectProviderServer struct {
	grpc.ServerStream
}

func (x *collectorConnectProviderServer) Send(m *Update_ToProvider) error {
	return x.ServerStream.SendMsg(m)
}

func (x *collectorConnectProviderServer) Recv() (*Update_FromProvider, error) {
	m := new(Update_FromProvider)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func _Collector_ConnectProcessor_Handler(srv interface{}, stream grpc.ServerStream) error {
	return srv.(CollectorServer).ConnectProcessor(&collectorConnectProcessorServer{stream})
}

type Collector_ConnectProcessorServer interface {
	Send(*Update_ToProcessor) error
	Recv() (*Update_FromProcessor, error)
	grpc.ServerStream
}

type collectorConnectProcessorServer struct {
	grpc.ServerStream
}

func (x *collectorConnectProcessorServer) Send(m *Update_ToProcessor) error {
	return x.ServerStream.SendMsg(m)
}

func (x *collectorConnectProcessorServer) Recv() (*Update_FromProcessor, error) {
	m := new(Update_FromProcessor)
	if err := x.ServerStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

var _Collector_serviceDesc = grpc.ServiceDesc{
	ServiceName: "tracking.Collector",
	HandlerType: (*CollectorServer)(nil),
	Methods:     []grpc.MethodDesc{},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "ConnectProvider",
			Handler:       _Collector_ConnectProvider_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
		{
			StreamName:    "ConnectProcessor",
			Handler:       _Collector_ConnectProcessor_Handler,
			ServerStreams: true,
			ClientStreams: true,
		},
	},
	Metadata: "tracking/tracking.proto",
}